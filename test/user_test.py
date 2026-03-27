from app.core.security import get_password_hash

password = "admin123"

hash_password = get_password_hash(password)

print(hash_password)