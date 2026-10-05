# Sprint 2 - DevSecOps & Image Vulnerability Management

## Trivy Installation

Trivy was installed using the official Trivy repository.

Check the installation:

trivy --version

## Execute the Scanning Script

For the vulnerable image:

./scan.sh sprint2-vulnerable Dockerfile.vulnerable

For the clean image:

./scan.sh sprint2-clean Dockerfile.clean

## Security Scan Configuration

The scan uses:

--severity HIGH,CRITICAL
--ignore-unfixed

The security gate uses:

--exit-code 1

HIGH or CRITICAL vulnerabilities cause the security gate to fail.

## Vulnerability Reports

The script displays the vulnerability report in table format in the terminal.

It also saves JSON and HTML reports:

reports/sprint2-vulnerable.json
reports/sprint2-clean.json
reports/sprint2-vulnerable.html
reports/sprint2-clean.html

The vulnerable report contains the detected vulnerabilities.

The clean report contains no HIGH or CRITICAL vulnerabilities.
