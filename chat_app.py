import socket
import threading
import sqlite3
import hashlib
import random
from math import gcd

# RSA Implementation

def generate_prime_candidate(length):
    p = 0
    while not is_prime(p):
        p = random.getrandbits(length)
    return p

def is_prime(n, k=128):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)
    return ((e, n), (d, n))

p = generate_prime_candidate(8)
q = generate_prime_candidate(8)

public_key, private_key = generate_keypair(p, q)

# Database Connection
conn = sqlite3.connect('chat_app.db')
cursor = conn.cursor()

# User Registration and Authentication

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    password_hash = hash_password(password)
    try:
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists.")

def authenticate_user(username, password):
    password_hash = hash_password(password)
    cursor.execute('SELECT * FROM users WHERE username = ? AND password_hash = ?', (username, password_hash))
    return cursor.fetchone() is not None

# Message Sending and Receiving

def encrypt(public_key, plaintext):
    e, n = public_key
    return [pow(ord(char), e, n) for char in plaintext]

def decrypt(private_key, ciphertext):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])

def sign(private_key, message):
    d, n = private_key
    hash_value = int.from_bytes(hashlib.sha256(message.encode()).digest(), byteorder='big')
    return pow(hash_value, d, n)

def verify(public_key, message, signature):
    e, n = public_key
    hash_value = int.from_bytes(hashlib.sha256(message.encode()).digest(), byteorder='big')
    return hash_value == pow(signature, e, n)

def send_message(sock, private_key, public_key, message):
    signature = sign(private_key, message)
    ciphertext = encrypt(public_key, message)
    sock.sendall(str(ciphertext).encode() + b'###' + str(signature).encode())

def receive_message(sock, private_key, public_key):
    data = sock.recv(1024)
    message, signature = data.split(b'###')
    message = eval(message.decode())
    signature = int(signature.decode())
    plaintext = decrypt(private_key, message)
    if verify(public_key, plaintext, signature):
        print("Message received: ", plaintext)
    else:
        print("Message verification failed.")

# User Interface

def user_interface():
    while True:
        choice = input("1. Register\n2. Log In\n3. Exit\nChoose an option: ")
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if authenticate_user(username, password):
                print("Logged in successfully.")
                if username == 'A':
                    start_chat(private_key, public_key)
                elif username == 'B':
                    start_chat(private_key, public_key)
            else:
                print("Authentication failed.")
        elif choice == '3':
            break

def start_chat(private_key, public_key):
    choice = input("1. Send Message\n2. Receive Message\nChoose an option: ")
    if choice == '1':
        host = input("Enter recipient IP: ")
        port = int(input("Enter recipient port: "))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            message = input("Enter message: ")
            send_message(s, private_key, public_key, message)
    elif choice == '2':
        host = '0.0.0.0'
        port = int(input("Enter port to listen on: "))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                receive_message(conn, private_key, public_key)

if __name__ == "__main__":
    user_interface()

