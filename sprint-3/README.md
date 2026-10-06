# Sprint 3 - Centralized Secrets Management with HashiCorp Vault

## Project Overview

This project demonstrates centralized secrets management using HashiCorp Vault.

Vault stores database credentials, and a Python script retrieves them dynamically at runtime instead of storing them in plain text or a static .env file.

## Tools Used

- HashiCorp Vault
- Docker
- Docker Compose
- Python
- Vault REST API

## Project Structure

    sprint-3/
    ├── docker-compose.yml
    ├── secret_fetcher.py
    └── README.md

## 1. Start Vault

Start the Vault server in Dev Mode:

    docker-compose up -d

Check the Vault container:

    docker-compose ps

Verify Vault status:

    docker exec -e VAULT_ADDR=http://127.0.0.1:8200 sprint3-vault vault status

Vault should be initialized and unsealed.

## 2. Store the Sample Database Secret

Vault Dev Mode provides the KV v2 secret engine at secret/.

Insert the dummy database secret:

    docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=sprint3-root-token sprint3-vault vault kv put secret/database username="demo_user" password="demo_password" connection_string="postgresql://localhost:5432/demo_db"

The secret is stored at:

    secret/data/database

The values above are dummy/test credentials.

## 3. Retrieve the Secret

Run the Python retrieval script:

    python3 secret_fetcher.py

The script authenticates with Vault using an API token, requests the secret through the Vault REST API, parses the response, and masks sensitive values in the terminal output.

Example output:

    Secret retrieved successfully!
    Username: de****er
    Password: de****rd
    Connection String: po****db

Sensitive values are masked to prevent leakage in terminal output.

## Security Note

Do not commit actual production secrets or tokens to the GitHub repository.
