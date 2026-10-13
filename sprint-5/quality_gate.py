import json
import sys

# Check SAST findings
with open("reports/sast-report.json") as file:
    sast_report = json.load(file)

blocking_findings = []

for finding in sast_report["results"]:
    metadata = finding["extra"].get("metadata", {})
    score = float(metadata.get("security-severity", 0))

    if score >= 7.0:
        blocking_findings.append(finding)

# Check dependency vulnerabilities
with open("reports/dependency-report.json") as file:
    dependency_report = json.load(file)

dependency_vulnerabilities = sum(
    len(package["vulns"])
    for package in dependency_report["dependencies"]
)

print("SAST HIGH/CRITICAL findings:", len(blocking_findings))
print("Dependency vulnerabilities:", dependency_vulnerabilities)

if blocking_findings or dependency_vulnerabilities:
    print("QUALITY GATE: FAILED")
    sys.exit(1)

print("QUALITY GATE: PASSED")
sys.exit(0)
