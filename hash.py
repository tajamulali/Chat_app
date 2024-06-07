def simple_hash(data):
    """
    A simple hash function.
    """
    hash_value = 0
    for char in data:
        hash_value = (hash_value * 31 + ord(char)) % (2**32)
    return hex(hash_value)
