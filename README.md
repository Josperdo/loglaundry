# Log Event Filter

A Python utility for analyzing authentication logs and identifying failed SSH login attempts.

## Overview

This project reads system log files (auth.log, syslog) and filters for security events, with a focus on failed SSH authentication attempts. It generates summary reports to assist with security monitoring and analysis.

## Current Status

Version 1.0 - Core filtering functionality

## Usage

```bash
python filter_v1.py
```

This reads `sample.log` and outputs lines containing failed password attempts.

## Project Goals

- Parse authentication logs efficiently
- Filter for security-relevant events
- Generate actionable summary reports
- Support multiple log formats

## Requirements

- Python 3.7+

## License

MIT License - see LICENSE file for details
