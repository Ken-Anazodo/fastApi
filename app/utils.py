from pwdlib import PasswordHash #pwdlib is a great Python package to handle password hashes.

password_hash = PasswordHash.recommended() # This creates a PasswordHash object that uses the recommended hashing algorithm. 

def hash(password: str):
    return password_hash.hash(password)

def verify(plain_password, hash_password):
    return password_hash.verify(plain_password, hash_password)
