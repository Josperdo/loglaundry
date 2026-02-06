# Log Event Filter

A Python utility for analyzing authentication logs and identifying failed SSH login attempts with IP tracking and repeat offender detection.

## Overview

This project reads system log files and analyzes failed SSH authentication attempts. It extracts IP addresses using regex pattern matching, tracks repeat offenders, and generates summary reports to assist with security monitoring and threat analysis.

## Features

**Current:**
- Parses authentication logs for failed password attempts
- Extracts IP addresses using regex pattern matching
- Tracks and counts repeat offenders
- Generates summary reports with attempt counts per IP
- Threshold-based alerts for high-risk IPs (configurable threshold)
- Exports data to CSV format with risk level indicators
- Exports data to structured JSON format with risk level metadata

**Planned:**
- Geolocation lookup for source IPs
- Support for multiple log formats
- Real-time log monitoring
- Configurable alert thresholds via command-line arguments

## Current Status

Version 2.0 - High-risk IP threshold alerts implemented

## Usage

```bash
python filter_v1.py
```

This reads `sample.log` and:
- Displays a terminal summary of failed login attempts by IP address
- Generates `exports/failed_logins.csv` with IP addresses, attempt counts, and risk levels
- Generates `exports/failed_logins.json` with structured data including total attempts

### Example Terminal Output

```
Failed login attempts by IP:
192.168.1.100: 5 attempts - HIGH RISK
10.0.0.25: 4 attempts - HIGH RISK
172.16.0.10: 2 attempts
192.168.1.105: 1 attempts
Total failed attempts: 12
High risk IPs detected: 2
```

The script flags IPs exceeding 3 failed attempts as HIGH RISK, helping security teams prioritize response efforts.

## Output Files

The script generates two output files in the `exports/` directory. See the `examples/` folder for sample output.

**failed_logins.csv** - Spreadsheet-compatible format
```csv
IP Address,Attempt Count,Risk_Level
192.168.1.100,5,HIGH RISK
10.0.0.25,4,HIGH RISK
172.16.0.10,2,NORMAL
192.168.1.105,1,NORMAL
```

**failed_logins.json** - Structured data format
```json
{
    "failed_logins": [
        {"IP Address": "192.168.1.100", "Attempt Count": 5, "Risk Level": "HIGH RISK"},
        {"IP Address": "10.0.0.25", "Attempt Count": 4, "Risk Level": "HIGH RISK"},
        {"IP Address": "172.16.0.10", "Attempt Count": 2, "Risk Level": "NORMAL"},
        {"IP Address": "192.168.1.105", "Attempt Count": 1, "Risk Level": "NORMAL"}
    ],
    "total_attempts": 12
}
```

## How It Works

1. Opens and reads the log file line by line
2. Filters for lines containing "Failed password"
3. Extracts IP addresses using regex pattern `\d+\.\d+\.\d+\.\d+`
4. Stores IPs in a dictionary with attempt counts
5. Evaluates each IP against the threshold (default: 3 attempts)
6. Displays summary report in terminal with HIGH RISK indicators
7. Counts and reports total high-risk IPs detected
8. Exports data to CSV file with risk level classifications
9. Exports data to structured JSON format with risk metadata

## Requirements

- Python 3.9+
- Standard library only (no external dependencies)

## License

MIT License - see LICENSE file for details
