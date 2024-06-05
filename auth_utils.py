import hashlib
import os

def hash_password(password):
    salt = os.urandom(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + pwdhash

def verify_password(stored_password, provided_password):
    salt = stored_password[:16]
    stored_pwdhash = stored_password[16:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return pwdhash == stored_pwdhash
  
