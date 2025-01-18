import secrets

# Genera una chiave segreta sicura
secret_key = secrets.token_hex(32)
print(secret_key)