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
- Exports data to CSV format (failed_logins.csv)
- Exports data to structured JSON format (failed_logins.json)

**Planned:**
- Threshold-based alerts for high-risk IPs
- Geolocation lookup for source IPs
- Support for multiple log formats
- Real-time log monitoring

## Current Status

Version 1.5 - CSV/JSON export functionality added

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
10.0.0.50: 1
203.0.113.45: 3
198.51.100.22: 2
Total failed attempts: 6
```

## Output Files

The script generates two output files in the `exports/` directory. See the `examples/` folder for sample output.

**failed_logins.csv** - Spreadsheet-compatible format
```csv
IP Address,Attempt Count
10.0.0.50,1
203.0.113.45,3
198.51.100.22,2
```

**failed_logins.json** - Structured data format
```json
{
    "failed_logins": [
        {"IP Address": "10.0.0.50", "Attempt Count": 1},
        {"IP Address": "203.0.113.45", "Attempt Count": 3},
        {"IP Address": "198.51.100.22", "Attempt Count": 2}
    ],
    "total_attempts": 6
}
```

## How It Works

1. Opens and reads the log file line by line
2. Filters for lines containing "Failed password"
3. Extracts IP addresses using regex pattern `\d+\.\d+\.\d+\.\d+`
4. Stores IPs in a dictionary with attempt counts
5. Displays summary report in terminal
6. Exports data to CSV file with headers and counts
7. Exports data to structured JSON format with metadata

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## License

MIT License - see LICENSE file for details
