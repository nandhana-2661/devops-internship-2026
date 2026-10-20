import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# Create test buckets if they do not already exist
existing = {b["Name"] for b in s3.list_buckets()["Buckets"]}

for bucket in ["sprint7-insecure-bucket", "sprint7-secure-bucket"]:
    if bucket not in existing:
        s3.create_bucket(Bucket=bucket)

# Insecure bucket: disable public access protection
s3.put_public_access_block(
    Bucket="sprint7-insecure-bucket",
    PublicAccessBlockConfiguration={
        "BlockPublicAcls": False,
        "IgnorePublicAcls": False,
        "BlockPublicPolicy": False,
        "RestrictPublicBuckets": False
    }
)

# Enable ACLs for the insecure test bucket
s3.put_bucket_ownership_controls(
    Bucket="sprint7-insecure-bucket",
    OwnershipControls={
        "Rules": [{"ObjectOwnership": "BucketOwnerPreferred"}]
    }
)

# Configure public-read ACL
s3.put_bucket_acl(
    Bucket="sprint7-insecure-bucket",
    ACL="public-read"
)

# Remove explicit encryption configuration
s3.delete_bucket_encryption(
    Bucket="sprint7-insecure-bucket"
)

# Secure bucket: block all public access
s3.put_public_access_block(
    Bucket="sprint7-secure-bucket",
    PublicAccessBlockConfiguration={
        "BlockPublicAcls": True,
        "IgnorePublicAcls": True,
        "BlockPublicPolicy": True,
        "RestrictPublicBuckets": True
    }
)

# Secure bucket: enable encryption
s3.put_bucket_encryption(
    Bucket="sprint7-secure-bucket",
    ServerSideEncryptionConfiguration={
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256"
                }
            }
        ]
    }
)

print("S3 test resources seeded successfully!")

# Create intentionally insecure Security Group
ec2 = boto3.client(
    "ec2",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

vpc_id = ec2.describe_vpcs(
    Filters=[{"Name": "is-default", "Values": ["true"]}]
)["Vpcs"][0]["VpcId"]

existing_groups = ec2.describe_security_groups(
    Filters=[
        {"Name": "group-name", "Values": ["sprint7-insecure-sg"]},
        {"Name": "vpc-id", "Values": [vpc_id]}
    ]
)["SecurityGroups"]

if existing_groups:
    sg_id = existing_groups[0]["GroupId"]
else:
    response = ec2.create_security_group(
        GroupName="sprint7-insecure-sg",
        Description="Intentionally insecure security group for Sprint 7",
        VpcId=vpc_id
    )
    sg_id = response["GroupId"]

# Add SSH exposure only if the rule does not already exist
sg = ec2.describe_security_groups(GroupIds=[sg_id])["SecurityGroups"][0]

ssh_open = any(
    rule["IpProtocol"] in ("tcp", "-1")
    and rule.get("FromPort", 0) <= 22 <= rule.get("ToPort", 65535)
    and any(ip["CidrIp"] == "0.0.0.0/0" for ip in rule.get("IpRanges", []))
    for rule in sg["IpPermissions"]
)

if not ssh_open:
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
            }
        ]
    )

print("Insecure Security Group seeded successfully!")

# Create intentionally unencrypted EBS volume
existing_volumes = ec2.describe_volumes(
    Filters=[
        {
            "Name": "tag:Name",
            "Values": ["sprint7-insecure-ebs"]
        }
    ]
)["Volumes"]

if not existing_volumes:
    response = ec2.create_volume(
        AvailabilityZone="us-east-1a",
        Size=1,
        VolumeType="gp3",
        Encrypted=False,
        TagSpecifications=[
            {
                "ResourceType": "volume",
                "Tags": [
                    {"Key": "Name", "Value": "sprint7-insecure-ebs"}
                ]
            }
        ]
    )
    print("Created EBS Volume:", response["VolumeId"])
else:
    print("Existing EBS Volume:", existing_volumes[0]["VolumeId"])

print("EBS test resource seeded successfully!")
