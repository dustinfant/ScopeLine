# Pentest Project

**Modular, scope-driven API penetration testing framework** focusing on identity, authorization, SSRF, and common vulnerabilities.

## Overview

This tool provides a structured approach to web application and API security testing. It is:

- **Scope-driven**: Load assets from `scope.yaml` to define targets.
- **Modular**: Separate discovery, vulnerability scanning, and reporting.
- **Extensible**: Easily add new modules for additional checks.

### Key Features

- HTTP and OpenAPI discovery
- Directory and endpoint enumeration
- JWT and authentication header analysis
- Privilege inference
- IDOR and SSRF vulnerability detection
- Markdown reporting of findings

## Usage

bash
# Ensure PYTHONPATH includes current directory
export PYTHONPATH=.

# Run full scan
python3 run.py

# Run CI-style scan
python3 run.py --ci

