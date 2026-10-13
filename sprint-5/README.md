# Sprint 5 – Static Application Security Testing (SAST) & Quality Gates

## Project Overview

This project integrates static application security testing and dependency vulnerability scanning into a GitHub Actions CI pipeline. The security quality gate fails when security issues are detected.

## Tools Used

- **Semgrep:** Scans Python source code using custom security rules.
- **pip-audit:** Checks Python dependencies for known vulnerabilities.
- **GitHub Actions:** Runs the security scans and quality gate in CI.

## Project Files

- `samples/clean.py` – Secure sample source code.
- `samples/vulnerable.py` – Intentionally vulnerable source code.
- `rules/security-rules.yml` – Custom Semgrep rules.
- `requirements.txt` – Updated dependencies for the clean scenario.
- `requirements.vulnerable.txt` – Vulnerable dependencies for testing.
- `scan.sh` – Runs both security scanners and the quality gate.
- `quality_gate.py` – Evaluates the generated security reports.
- `reports/` – JSON audit reports.
- `screenshots/` – Local FAIL and PASS evidence.

The GitHub Actions workflow is located at `.github/workflows/sprint5-sast.yml` in the repository root, as required by GitHub Actions.

## SAST Configuration and Custom Rules

Semgrep uses `rules/security-rules.yml` to detect:

1. Hardcoded passwords.
2. Potential SQL injection.
3. Insecure pickle deserialization.

The rules include security severity scores. To customize a rule, edit its detection pattern or `security-severity` metadata in the YAML file.

Validate the rules:

```bash
semgrep --validate --config rules/security-rules.yml
```

## Dependency Scanning

pip-audit scans the packages listed in `requirements.txt`.

The intentionally vulnerable dependency version is stored in `requirements.vulnerable.txt` for the FAIL scenario.

## Run Locally

From the `sprint-5` directory, activate the Python virtual environment and install the tools:

```bash
source .venv/bin/activate
python -m pip install semgrep==1.180.0 pip-audit==2.10.1
```

Run the vulnerable source code scan:

```bash
cp requirements.vulnerable.txt requirements.txt
./scan.sh samples/vulnerable.py
```

Run the clean source code scan after restoring the updated dependency:

```bash
echo 'requests==2.34.2' > requirements.txt
./scan.sh samples/clean.py
```

The scan script generates `reports/sast-report.json` and `reports/dependency-report.json`.

## Security Quality Gate

`quality_gate.py` reads both JSON reports.

- SAST findings with a security severity score of **7.0 or higher** (HIGH/CRITICAL) fail the quality gate.
- The dependency scanner fails the quality gate if **any known dependency vulnerability** is found.
- A failed quality gate exits with code `1`, causing the CI job to fail.
- A successful quality gate exits with code `0`.

## GitHub Actions CI

The workflow runs automatically when Sprint 5 files or its workflow configuration are pushed.

It also supports manual execution using **Actions → Sprint 5 - Security Scanning → Run workflow**, with two scenarios:

- `clean` – Runs the clean source and updated dependency scan; expected to PASS.
- `vulnerable` – Runs the intentionally vulnerable source and dependency scan; expected to FAIL.

Security reports are uploaded as CI artifacts even when the scan job fails.

## Proof of Work

Local terminal screenshots:

- `screenshots/sprint5-local-fail.png` – Vulnerable scan fails the quality gate.
- `screenshots/sprint5-local-pass.png` – Clean scan passes the quality gate.

GitHub Actions CI screenshots:

- `screenshots/sprint5-ci-fail.png` – CI fails when security vulnerabilities are detected.
- `screenshots/sprint5-ci-pass.png` – CI passes when no security vulnerabilities are detected.

The GitHub Actions run logs also provide CI PASS/FAIL evidence.
