import secrets

# Generate a secure random string of 32 bytes (256 bits)
secret_key = secrets.token_hex(32)

print(f"Generated SECRET_KEY: {secret_key}")
