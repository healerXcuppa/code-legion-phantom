"""Generator / Utility functions for the Bank System project."""
import secrets
from datetime import datetime, timezone

def generate_customer_id():
    """Generates and returns ID for each customer"""

    # Stores the secret string combinations derived
    retrieved_values = secrets.token_hex(8)

    # Joining the numbers together to get a customer ID
    new_customer_id = "CUST-" + retrieved_values.upper()

    # Returning the generated customer ID
    return new_customer_id

def generate_account_number():
    """Generates and returns account number for each account"""
    # Stores each secret string number gotten on each loop turn
    retrieved_values = []

    # Loop to get 10 secret string numbers
    for _ in range(10):
        secret_number = secrets.choice("0123456789")
        retrieved_values.append(secret_number)

    # Joining the numbers together to get an account number
    new_account_number = "000" + "".join(retrieved_values)

    # Returning the generated account number
    return new_account_number

def generate_transaction_id():
    """Creates and Returns a unique transaction id sequence"""
    # Generating a unique transaction id using secrets module
    unique_transaction_id = secrets.token_hex(8)

    # Adding a prefix to the generated transaction id
    new_transaction_id = "TXN-" + unique_transaction_id.upper()

    # Returning the generated transaction id
    return new_transaction_id

def generate_timestamp():
    """Generates a standardized UTC ISO-8601 timestamp string for audit logs."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")