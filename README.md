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
- Generates `failed_logins.csv` with IP addresses and attempt counts
- Generates `failed_logins.json` with structured data including total attempts

### Example Terminal Output

```
Failed login attempts by IP:
10.0.0.50: 1 attempts
203.0.113.45: 5 attempts - HIGH RISK
198.51.100.22: 2 attempts
Total failed attempts: 8
High risk IPs detected: 1
```

The script flags IPs exceeding 3 failed attempts as HIGH RISK, helping security teams prioritize response efforts.

## Output Files

The script generates two output files in the `exports/` directory. See the `examples/` folder for sample output.

**failed_logins.csv** - Spreadsheet-compatible format
```csv
IP Address,Attempt Count,Risk_Level
10.0.0.50,1,NORMAL
203.0.113.45,5,HIGH RISK
198.51.100.22,2,NORMAL
```

**failed_logins.json** - Structured data format
```json
{
    "failed_logins": [
        {"IP Address": "10.0.0.50", "Attempt Count": 1, "Risk Level": "NORMAL"},
        {"IP Address": "203.0.113.45", "Attempt Count": 5, "Risk Level": "HIGH RISK"},
        {"IP Address": "198.51.100.22", "Attempt Count": 2, "Risk Level": "NORMAL"}
    ],
    "total_attempts": 8
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

- Python 3.7+
- Standard library only (no external dependencies)

## License

MIT License - see LICENSE file for details
