import socket
import threading
import json
from rsa import generate_keys, sign_message, verify_signature
from database import register_user, validate_login, save_message, get_messages, store_public_key, get_public_key

def handle_client(client_socket):
    try:
        message = client_socket.recv(1024).decode('utf-8')
        if message.startswith("REGISTER"):
            _, username, password = message.split(" ", 2)
            if register_user(username, password):
                client_socket.send("Registration successful".encode('utf-8'))
            else:
                client_socket.send("Registration failed".encode('utf-8'))
        elif message.startswith("LOGIN"):
            _, username, password = message.split(" ", 2)
            if validate_login(username, password):
                client_socket.send("Login successful".encode('utf-8'))
            else:
                client_socket.send("Login failed".encode('utf-8'))
        elif message.startswith("MESSAGE"):
            _, sender, recipient, message_content = message.split(" ", 3)
            save_message(sender, f"{sender}: {message_content}")
            client_socket.send("Message saved".encode('utf-8'))
        elif message.startswith("SEND_PUBLIC_KEY"):
            _, username, public_key = message.split(" ", 2)
            store_public_key(username, public_key)
            client_socket.send("Public key stored".encode('utf-8'))
        elif message.startswith("GET_PUBLIC_KEY"):
            _, username = message.split(" ", 1)
            public_key = get_public_key(username)
            if public_key:
                client_socket.send(public_key.encode('utf-8'))
            else:
                client_socket.send("Public key not found".encode('utf-8'))
        elif message.startswith("SEND_MESSAGE_ENCRYPTED"):
            _, sender, recipient, encrypted_message = message.split(" ", 3)
            recipient_public_key = get_public_key(recipient)
            if recipient_public_key:
                decrypted_message = decrypt_message(recipient_public_key, encrypted_message)
                save_message(sender, f"{sender}: {decrypted_message}")
                client_socket.send("Message saved".encode('utf-8'))
            else:
                client_socket.send("Recipient not found".encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_peer(host='127.0.0.1', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Peer started on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def encrypt_message(recipient_public_key, message):
    # Implement RSA encryption here
    pass

def decrypt_message(private_key, encrypted_message):
    # Implement RSA decryption here
    pass

if __name__ == "__main__":
    start_peer()
