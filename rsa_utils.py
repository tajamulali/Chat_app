import random

def generate_prime_candidate(length):
    p = 0
    while p % 2 == 0 or not is_prime(p):
        p = random.getrandbits(length)
    return p

def is_prime(n, k=5):  # number of tests = 5
    if n < 2:
        return False
    for _ in range(k):
        a = random.randint(1, n - 1)
        if pow(a, n - 1, n) != 1:
            return False
    return True

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_rsa_keypair(key_size):
    e = 65537
    p = generate_prime_candidate(key_size // 2)
    q = generate_prime_candidate(key_size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    d = modinv(e, phi)
    public_key = (e, n)
    private_key = (d, n)
    
    return public_key, private_key

def rsa_encrypt(message, public_key):
    e, n = public_key
    message_int = int.from_bytes(message, byteorder='big')
    encrypted_int = pow(message_int, e, n)
    return encrypted_int.to_bytes((encrypted_int.bit_length() + 7) // 8, byteorder='big')

def rsa_decrypt(ciphertext, private_key):
    d, n = private_key
    ciphertext_int = int.from_bytes(ciphertext, byteorder='big')
    decrypted_int = pow(ciphertext_int, d, n)
    return decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, byteorder='big')

def rsa_sign(message_hash, private_key):
    return rsa_encrypt(message_hash, private_key)

def rsa_verify(message_hash, signature, public_key):
    decrypted_hash = rsa_decrypt(signature, public_key)
    return decrypted_hash == message_hash
  
