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

**Planned:**
- Threshold-based alerts for high-risk IPs
- Export to CSV/JSON formats
- Geolocation lookup for source IPs
- Support for multiple log formats

## Current Status

Version 1.0 - IP extraction and repeat offender tracking

## Usage

```bash
python filter_v1.py
```

This reads `sample.log` and outputs:
- A summary of failed login attempts by IP address
- Count of attempts per IP
- Total number of failed attempts

### Example Output

```
Failed login attempts by IP:
10.0.0.50: 1
203.0.113.45: 3
198.51.100.22: 2
Total failed attempts: 6
```

## How It Works

1. Opens and reads the log file line by line
2. Filters for lines containing "Failed password"
3. Extracts IP addresses using regex pattern `\d+\.\d+\.\d+\.\d+`
4. Stores IPs in a dictionary with attempt counts
5. Displays summary report after processing

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## License

MIT License - see LICENSE file for details
