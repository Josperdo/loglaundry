# Loglaundry

A Python utility for surfacing SSH brute force and credential stuffing patterns from authentication logs.

---

## The Threat

SSH brute force and credential stuffing are among the most consistent initial access techniques in the wild. Attackers — ranging from opportunistic scanners to targeted threat actors — routinely automate login attempts against internet-exposed SSH services using wordlists of common usernames (`root`, `admin`, `deploy`) and leaked credential databases.

The behavioral signature is predictable: **multiple failed authentication attempts from a single source IP, often targeting multiple distinct usernames in rapid succession.** This multi-account targeting is what distinguishes automated tooling from a user who forgot their password. A legitimate user fails twice on one account. A credential stuffing tool cycles through `admin`, `root`, `ubuntu`, `user`, and `guest` in under ninety seconds.

At the log level, OpenSSH records each failure in `/var/log/auth.log` (or its journal equivalent):

```
Feb  1 08:15:23 server sshd[1234]: Failed password for admin from 192.168.1.100 port 45678 ssh2
Feb  1 08:15:45 server sshd[1235]: Failed password for root from 192.168.1.100 port 45679 ssh2
Feb  1 08:16:45 server sshd[1237]: Failed password for user from 192.168.1.100 port 45681 ssh2
```

Three failed attempts, three different usernames, 89 seconds — that's not a confused admin.

**Relevant MITRE ATT&CK techniques:**
- [T1110.001](https://attack.mitre.org/techniques/T1110/001/) — Brute Force: Password Guessing
- [T1110.003](https://attack.mitre.org/techniques/T1110/003/) — Brute Force: Password Spraying
- Tactic: Initial Access

---

## How Detection Works

### The Detection Hypothesis

> If a source IP generates more than N failed SSH authentication attempts within the observed log window, that IP is exhibiting behavior consistent with automated credential attacks and warrants investigation.

Loglaundry operationalizes this hypothesis in three steps:

**1. Filter for failure events**

The tool scans each log line for the string `Failed password` — the literal token OpenSSH writes on every failed password authentication. Lines containing successful logins (`Accepted publickey`, `Accepted password`), connection lifecycle events, and account lockout messages are ignored.

**2. Extract and aggregate by source IP**

For each matching line, a regex extracts the source IPv4 address and increments a per-IP counter. The result is a frequency map: how many times did each IP fail to authenticate?

**3. Apply threshold-based risk classification**

IPs exceeding the threshold (default: 3 attempts) are flagged `HIGH RISK`. The threshold is intentionally low — the goal is to surface candidates for human triage, not to auto-block. A single high-volume attacker generating 50 attempts will look identical in the output to one generating 4; both need a response.

### What the Code Does Not Do

Understanding limitations is part of detection engineering. This tool:

- **Does not analyze timing.** It treats the entire log as one window. A distributed slow attack (one attempt per hour) with four source IPs will not surface a single `HIGH RISK` flag even if all four are coordinated.
- **Does not correlate usernames.** Multi-account targeting from one IP is a stronger signal than single-account brute force. That signal is visible in the underlying logs but not reflected in the current output.
- **Does not validate extracted IPs.** The regex matches the first IPv4-shaped string on a matching line. Unusual log formats could return the wrong IP.
- **Does not parse log timestamps.** All failures are treated as contemporaneous.

These are documented tradeoffs for the current scope, not oversights.

---

## Example Detection

### Input Log (`sample.log`)

```
Feb  1 08:15:23 server sshd[1234]: Failed password for admin from 192.168.1.100 port 45678 ssh2
Feb  1 08:15:45 server sshd[1235]: Failed password for root from 192.168.1.100 port 45679 ssh2
Feb  1 08:16:12 server sshd[1236]: Accepted publickey for ubuntu from 192.168.1.50 port 45680 ssh2
Feb  1 08:16:45 server sshd[1237]: Failed password for user from 192.168.1.100 port 45681 ssh2
Feb  1 08:17:10 server sshd[1238]: Connection closed by authenticating user ubuntu 192.168.1.50 port 45682 [preauth]
Feb  1 08:17:33 server sshd[1239]: Failed password for admin from 10.0.0.25 port 45683 ssh2
Feb  1 08:18:01 server sshd[1240]: Accepted password for ubuntu from 192.168.1.50 port 45684 ssh2
Feb  1 08:18:45 server sshd[1241]: Failed password for root from 192.168.1.100 port 45685 ssh2
Feb  1 08:19:12 server sshd[1242]: User not allowed because account is locked
Feb  1 08:19:33 server sshd[1243]: Failed password for testuser from 10.0.0.25 port 45686 ssh2
Feb  1 08:20:15 server sshd[1244]: Failed password for root from 10.0.0.25 port 45687 ssh2
Feb  1 08:21:02 server sshd[1245]: Failed password for deploy from 172.16.0.10 port 45688 ssh2
Feb  1 08:21:45 server sshd[1246]: Failed password for admin from 192.168.1.100 port 45689 ssh2
Feb  1 08:22:10 server sshd[1247]: Accepted publickey for deploy from 172.16.0.10 port 45690 ssh2
Feb  1 08:22:33 server sshd[1248]: Failed password for root from 10.0.0.25 port 45691 ssh2
Feb  1 08:23:01 server sshd[1249]: Failed password for admin from 172.16.0.10 port 45692 ssh2
Feb  1 08:23:45 server sshd[1250]: Failed password for guest from 192.168.1.105 port 45693 ssh2
```

### Terminal Output

```
Failed login attempts by IP:
192.168.1.100: 5 attempts - HIGH RISK
10.0.0.25: 4 attempts - HIGH RISK
172.16.0.10: 2 attempts
192.168.1.105: 1 attempts
Total failed attempts: 12
High risk IPs detected: 2
```

### Reading the Output

**`192.168.1.100` — 5 attempts, HIGH RISK**
Targeted accounts in order: `admin → root → user → root → admin`. Cycling through a username wordlist. The repeated targeting of `root` and `admin` is consistent with a tool iterating through a top-N credential list. This is the highest-priority response candidate.

**`10.0.0.25` — 4 attempts, HIGH RISK**
Targeted accounts: `admin → testuser → root → root`. The inclusion of `testuser` alongside common admin accounts suggests a broader wordlist, potentially credential stuffing from a leaked database rather than a generic scanner.

**`172.16.0.10` — 2 attempts, NORMAL**
Failed on `deploy`, then succeeded via publickey. Likely a legitimate service account with a misconfigured password-auth fallback, not an attacker. Context from the surrounding log lines is what makes this distinguishable — a good reminder that the frequency count is a triage signal, not a verdict.

**`192.168.1.105` — 1 attempt, NORMAL**
Single failure on `guest`. Insufficient signal on its own.

---

## Output Files

Results are exported to `exports/` for downstream use.

**`exports/failed_logins.csv`**
```csv
IP Address,Attempt Count,Risk_Level
192.168.1.100,5,HIGH RISK
10.0.0.25,4,HIGH RISK
172.16.0.10,2,NORMAL
192.168.1.105,1,NORMAL
```

**`exports/failed_logins.json`**
```json
{
    "failed_logins": [
        {"IP Address": "192.168.1.100", "Attempt Count": 5, "Risk Level": "HIGH RISK"},
        {"IP Address": "10.0.0.25",     "Attempt Count": 4, "Risk Level": "HIGH RISK"},
        {"IP Address": "172.16.0.10",   "Attempt Count": 2, "Risk Level": "NORMAL"},
        {"IP Address": "192.168.1.105", "Attempt Count": 1, "Risk Level": "NORMAL"}
    ],
    "total_attempts": 12
}
```

The structured JSON output is intended for ingestion into downstream tooling — a SIEM, a ticketing system, or a threat intel enrichment pipeline that can correlate flagged IPs against known blocklists.

---

## Setup and Usage

**Requirements:** Python 3.9+, standard library only (no external dependencies)

```bash
git clone https://github.com/yourusername/loglaundry.git
cd loglaundry
python filter_v1.py
```

By default, the script reads `sample.log` from the current directory. To analyze a real auth log, replace `sample.log` with your target file or symlink it:

```bash
# Linux systems using syslog
cp /var/log/auth.log sample.log
python filter_v1.py

# Or on systemd-based systems
journalctl -u ssh --no-pager > sample.log
python filter_v1.py
```

Output is written to `exports/failed_logins.csv` and `exports/failed_logins.json`. The `exports/` directory is created automatically if it does not exist.

---

## Planned Improvements

- **Configurable threshold and input path via CLI arguments** — removes hardcoded values, enables scripted use
- **Username aggregation per source IP** — surfaces multi-account targeting as a first-class signal
- **Timestamp-aware windowing** — detect rate-of-fire patterns, not just raw totals
- **Multiple log format support** — extend beyond OpenSSH syslog to `journald`, `fail2ban`, and cloud provider auth logs
- **IP enrichment** — geolocation and ASN lookups to add context to flagged sources

---

## License

MIT — see [LICENSE](LICENSE)
