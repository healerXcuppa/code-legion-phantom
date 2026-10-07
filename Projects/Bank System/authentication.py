"""Authentication and credential security for the Bank System project."""
import secrets
import hashlib

# Setting a global iteration count variable for efficiency
iteration_count = 600000
hash_name = "sha256"
algorithm = f"pbkdf2_{hash_name}"

def hash_helper(credential_input):
    """Generates salt and hash strings to be returned"""
    # Salt value for randomized bytes
    raw_salt = secrets.token_bytes(16)

    # Hash bytes stores raw binary output of the hashed password/pin and salt values
    new_hash_bytes = hashlib.pbkdf2_hmac(
        hash_name,
        credential_input.encode("utf-8"),
        raw_salt,
        iteration_count
    )

    # Formating hash bytes to hash string
    hash_string = new_hash_bytes.hex()
    hex_salt = raw_salt.hex()

    # Returning salt value and hashed _string
    return f"{algorithm}:{iteration_count}:{hex_salt}:{hash_string}"

def verification_helper(stored_credential,user_credential):
    """Checks validity of user credentials"""

    # Split stored credentials and handle invalid value appropriately
    try:
        # 1. Unpack exact 4 parts
        stored_algorithm, stored_iteration, stored_salt, stored_hash = stored_credential.split(":")

        # 2. Convert iterations string to integer
        iteration_count_int = int(stored_iteration)

        # 3. Convert hex salt string back to raw bytes
        raw_salt = bytes.fromhex(stored_salt)

    except ValueError as error_message:
        # Handles missing colons, non-integer iterations, or non-hex salt strings
        print(f"Error parsing credential record: {error_message}")
        return False

    # Validating the algorithm match
    if not secrets.compare_digest(stored_algorithm,algorithm):
        return False

    # Rehashing user credentials
    re_hash = hashlib.pbkdf2_hmac(
        stored_algorithm.split("_")[1],
        user_credential.encode("utf-8"),
        raw_salt,
        iteration_count_int
    )

    # Converting rehashed value to string
    re_hashed = re_hash.hex()

    # Returning Boolean value upon comparison
    return secrets.compare_digest(stored_hash,re_hashed)

def hash_password(user_password):
    """Returns a salted and hashed representation of the PASSWORD."""
    return hash_helper(user_password)

def verify_password(stored_password,user_password_input):
    """Returns True/False for password verification"""
    return verification_helper(stored_password,user_password_input)

def hash_pin(user_pin):
    """Returns a salted and hashed representation of the PIN."""
    return hash_helper(user_pin)

def verify_pin(stored_pin,user_pin_input):
    """Returns True or False for pin verification"""
    return verification_helper(stored_pin,user_pin_input)

def change_password(stored_password, old_password_input, new_password_input):
    """Returns a new password hash if the old password is valid."""

    # Conditional logic to take and store new password
    if verification_helper(stored_password,old_password_input):
        return hash_helper(new_password_input)
    return None

def change_pin(stored_pin, old_pin_input, new_pin_input):
    """Returns a new hashed pin if the old pin is valid."""

    # Conditional logic to take and store new pin
    if verify_pin(stored_pin,old_pin_input):
        return hash_helper(new_pin_input)
    return None