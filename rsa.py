import random

def generate_keys():
    # This is a simplified RSA key generation for educational purposes.
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17  # Choose e
    d = pow(e, -1, phi)
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key

def sign_message(private_key, message):
    d, n = private_key
    message_int = int.from_bytes(message.encode(), 'big')
    signature = pow(message_int, d, n)
    return hex(signature)

def verify_signature(public_key, message, signature):
    e, n = public_key
    message_int = int.from_bytes(message.encode(), 'big')
    signature_int = int(signature, 16)
    verified_message = pow(signature_int, e, n)
    return message_int == verified_message
