from hash import simple_hash

def generate_keys():
    # Generate two large prime numbers (for demonstration purposes, we're using small numbers)
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e such that 1 < e < phi and e is coprime to phi
    e = 17
    d = pow(e, -1, phi)
    
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key

def sign_message(private_key, message):
    d, n = private_key
    hash_value = int(simple_hash(message), 16)
    signature = pow(hash_value, d, n)
    return signature

def verify_signature(public_key, message, signature):
    e, n = public_key
    hash_value = int(simple_hash(message), 16)
    hash_from_signature = pow(signature, e, n)
    return hash_value == hash_from_signature
