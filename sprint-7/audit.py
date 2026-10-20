import boto3
import json
from pathlib import Path
from botocore.exceptions import ClientError

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

audit_results = []

PUBLIC_GROUPS = {
    "http://acs.amazonaws.com/groups/global/AllUsers",
    "http://acs.amazonaws.com/groups/global/AuthenticatedUsers"
}

def audit_s3():
    print("\n=== S3 STORAGE EXPOSURE AUDIT ===")

    buckets = s3.list_buckets()["Buckets"]

    for bucket in buckets:
        name = bucket["Name"]
        issues = []

        # Check public access block
        try:
            response = s3.get_public_access_block(Bucket=name)
            config = response["PublicAccessBlockConfiguration"]

            if not all([
                config.get("BlockPublicAcls", False),
                config.get("IgnorePublicAcls", False),
                config.get("BlockPublicPolicy", False),
                config.get("RestrictPublicBuckets", False)
            ]):
                issues.append("Public access protection incomplete")

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchPublicAccessBlockConfiguration":
                issues.append("Public access block missing")
            else:
                raise

        # Check public ACL permissions
        acl = s3.get_bucket_acl(Bucket=name)

        for grant in acl["Grants"]:
            grantee = grant["Grantee"]

            if (
                grantee.get("Type") == "Group"
                and grantee.get("URI") in PUBLIC_GROUPS
                and grant["Permission"] in ("READ", "WRITE", "FULL_CONTROL")
            ):
                issues.append(
                    f"Public ACL permission: {grant['Permission']}"
                )

        if issues:
            print(f"\n[FAIL] Bucket: {name}")
            for issue in issues:
                print("Issue:", issue)
        else:
            print(f"\n[PASS] Bucket: {name}")

        audit_results.append({
            "resource": name,
            "check": "S3 Storage Exposure",
            "status": "FAIL" if issues else "PASS",
            "severity": "HIGH" if issues else None,
            "issues": issues,
            "remediation": (
                "Enable all S3 public access block settings and remove public ACL permissions."
                if issues else "No action required."
            )
        })

def audit_security_groups():
    print("\n=== NETWORK EXPOSURE AUDIT ===")

    ec2 = boto3.client(
        "ec2",
        endpoint_url="http://localhost:4566",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )

    sensitive_ports = {
        22: "SSH",
        3389: "RDP",
        3306: "MySQL",
        5432: "PostgreSQL"
    }

    groups = ec2.describe_security_groups()["SecurityGroups"]

    for sg in groups:
        issues = []

        for rule in sg["IpPermissions"]:
            protocol = rule.get("IpProtocol")

            if protocol not in ("tcp", "-1"):
                continue

            start = rule.get("FromPort", 0)
            end = rule.get("ToPort", 65535)

            for ip in rule.get("IpRanges", []):
                if ip.get("CidrIp") != "0.0.0.0/0":
                    continue

                for port, service in sensitive_ports.items():
                    if protocol == "-1" or start <= port <= end:
                        issues.append(
                            f"{service} port {port} open to 0.0.0.0/0"
                        )

        if issues:
            print(f"\n[FAIL] Security Group: {sg['GroupName']}")
            print("Group ID:", sg["GroupId"])

            for issue in issues:
                print("Issue:", issue)
        else:
            print(f"\n[PASS] Security Group: {sg['GroupName']}")

        audit_results.append({
            "resource": sg["GroupName"],
            "resource_id": sg["GroupId"],
            "check": "Network Exposure",
            "status": "FAIL" if issues else "PASS",
            "severity": "CRITICAL" if issues else None,
            "issues": issues,
            "remediation": (
                "Restrict sensitive inbound ports to trusted IP addresses."
                if issues else "No action required."
            )
        })

def audit_encryption():
    print("\n=== ENCRYPTION GAP AUDIT ===")

    ec2 = boto3.client(
        "ec2",
        endpoint_url="http://localhost:4566",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )

    # Check S3 encryption configuration
    for bucket in s3.list_buckets()["Buckets"]:
        name = bucket["Name"]

        try:
            response = s3.get_bucket_encryption(Bucket=name)
            rules = response.get(
                "ServerSideEncryptionConfiguration", {}
            ).get("Rules", [])

            if rules:
                print(f"\n[PASS] S3 Encryption: {name}")
            else:
                print(f"\n[FAIL] S3 Encryption: {name}")
                print("Issue: Explicit encryption configuration missing")

            audit_results.append({
                "resource": name,
                "check": "S3 Encryption Configuration",
                "status": "PASS" if rules else "FAIL",
                "severity": None if rules else "HIGH",
                "issues": [] if rules else [
                    "Explicit encryption configuration missing"
                ],
                "remediation": (
                    "No action required." if rules else
                    "Configure explicit default bucket encryption."
                )
            })

        except ClientError as e:
            if e.response["Error"]["Code"] in (
                "ServerSideEncryptionConfigurationNotFoundError",
                "NoSuchEncryptionConfiguration"
            ):
                print(f"\n[FAIL] S3 Encryption: {name}")
                print("Issue: Explicit encryption configuration missing")
                audit_results.append({
                    "resource": name,
                    "check": "S3 Encryption Configuration",
                    "status": "FAIL",
                    "severity": "HIGH",
                    "issues": ["Explicit encryption configuration missing"],
                    "remediation": "Configure explicit default bucket encryption."
                })
            else:
                raise

    # Check EBS encryption
    volumes = ec2.describe_volumes()["Volumes"]

    for volume in volumes:
        volume_id = volume["VolumeId"]

        if volume.get("Encrypted", False):
            print(f"\n[PASS] EBS Volume: {volume_id}")
        else:
            print(f"\n[FAIL] EBS Volume: {volume_id}")
            print("Issue: EBS volume encryption disabled")

        encrypted = volume.get("Encrypted", False)

        audit_results.append({
            "resource": volume_id,
            "check": "EBS Encryption",
            "status": "PASS" if encrypted else "FAIL",
            "severity": None if encrypted else "HIGH",
            "issues": [] if encrypted else [
                "EBS volume encryption disabled"
            ],
            "remediation": (
                "No action required." if encrypted else
                "Create an encrypted replacement volume using an encrypted snapshot."
            )
        })


if __name__ == "__main__":
    audit_results.clear()

    audit_s3()
    audit_security_groups()
    audit_encryption()

    report = {
        "project": "Sprint 7 - Cloud Security Posture Management",
        "environment": "LocalStack",
        "summary": {
            "total_checks": len(audit_results),
            "passed": sum(
                r["status"] == "PASS" for r in audit_results
            ),
            "failed": sum(
                r["status"] == "FAIL" for r in audit_results
            )
        },
        "findings": audit_results
    }

    Path("reports").mkdir(exist_ok=True)

    report_path = Path("reports/compliance-report.json")

    report_path.write_text(
        json.dumps(report, indent=2) + "\n"
    )

    print("\n=== COMPLIANCE REPORT ===")
    print("Total Checks:", report["summary"]["total_checks"])
    print("Passed:", report["summary"]["passed"])
    print("Failed:", report["summary"]["failed"])
    print("Report saved to:", report_path)
