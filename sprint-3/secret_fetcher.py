import os
import json
import urllib.request

VAULT_ADDR = "http://127.0.0.1:8200"
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "sprint3-root-token")
SECRET_PATH = "/v1/secret/data/database"


def mask(value):
    if not value:
        return "****"
    if len(value) <= 4:
        return "****"
    return value[:2] + "****" + value[-2:]


request = urllib.request.Request(
    VAULT_ADDR + SECRET_PATH,
    headers={
        "X-Vault-Token": VAULT_TOKEN
    }
)

try:
    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode())

    secret = result["data"]["data"]

    print("Secret retrieved successfully!")
    print(f"Username: {mask(secret['username'])}")
    print(f"Password: {mask(secret['password'])}")
    print(f"Connection String: {mask(secret['connection_string'])}")

except Exception as e:
    print(f"Failed to retrieve secret: {e}")
