# Sprint 7 – Cloud Security Posture Management (CSPM) & Automated Auditing

## Project Overview

This project implements an automated cloud security auditing tool using Python, boto3, and LocalStack. It scans simulated AWS infrastructure for critical security misconfigurations and generates a JSON compliance report.

## Technologies Used

- Python 3
- boto3
- Docker Compose
- LocalStack (simulated AWS S3 and EC2)

## Security Checks

1. **Storage Exposure:** Detects incomplete S3 Public Access Block settings and public ACL permissions.
2. **Network Exposure:** Detects Security Groups allowing unrestricted access (`0.0.0.0/0`) to ports 22, 3389, 3306, and 5432.
3. **Encryption Gaps:** Checks explicit S3 bucket encryption configuration and detects unencrypted EBS volumes.

Note: Missing explicit S3 encryption configuration is reported as a configuration gap, not proof that stored objects are unencrypted.

## Prerequisites

- Docker and Docker Compose
- Python 3 with venv support

Install the Python dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install boto3
```

## Start LocalStack

```bash
docker compose up -d
docker compose ps
```

LocalStack endpoint: `http://localhost:4566`

## Seed Test Resources

```bash
python seed.py
```

This script prepares intentionally insecure and secure test resources in LocalStack, including S3 buckets, a Security Group, and an EBS volume.

No real AWS account is required.

## Run the Security Audit

```bash
python audit.py
```

The scanner displays PASS/FAIL results and generates the compliance report.

## Compliance Report

Output file: `reports/compliance-report.json`

Each finding contains the resource, security check, PASS/FAIL status, severity (CRITICAL/HIGH for failures), detected issues, and remediation advice.

View or validate the report:

```bash
python -m json.tool reports/compliance-report.json
```

## Proof of Work

Screenshots of the terminal audit results and generated compliance report are included in the `screenshots/` directory.
