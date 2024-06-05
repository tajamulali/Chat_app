import random
from math import gcd
import hashlib

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_large_prime(key_size):
    while True:
        prime_candidate = random.getrandbits(key_size)
        if is_prime(prime_candidate):
            return prime_candidate

def generate_key_pair(key_size=2048):
    p = generate_large_prime(key_size // 2)
    q = generate_large_prime(key_size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # Common choice for e
    d = pow(e, -1, phi)

    return (e, n), (d, n)  # Public and Private keys

def hash_message(message):
    return hashlib.sha256(message.encode()).digest()

def sign_message(private_key, message):
    d, n = private_key
    message_hash = int.from_bytes(hash_message(message), byteorder='big')
    signature = pow(message_hash, d, n)
    return signature

def verify_message(public_key, message, signature):
    e, n = public_key
    message_hash = int.from_bytes(hash_message(message), byteorder='big')
    hash_from_signature = pow(signature, e, n)
    return message_hash == hash_from_signature
