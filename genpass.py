from werkzeug.security import generate_password_hash, check_password_hash

# Password to hash
password = "12345"

# Generate the hash
hash_value = generate_password_hash(password)
print("Generated hash:", hash_value)

# Verify the password against the hash
is_valid = check_password_hash(hash_value, password)
print("Verification result:", is_valid)