#!/bin/bash
set -e

TARGET="${1:-samples/vulnerable.py}"

echo "Running SAST scan..."
semgrep scan --config rules/security-rules.yml \
    --json --output reports/sast-report.json "$TARGET"

echo "Running dependency scan..."
pip-audit -r requirements.txt \
    -f json -o reports/dependency-report.json || true

echo "Checking security quality gate..."
python quality_gate.py
