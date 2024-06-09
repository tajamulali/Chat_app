import socket
import threading
import json
from database import register_user, validate_login, store_public_key, get_public_key

def handle_client(client_socket):
    try:
        message = client_socket.recv(1024).decode('utf-8')
        if message.startswith("REGISTER"):
            _, username, password_hash, public_key_str = message.split(" ", 3)
            public_key = json.loads(public_key_str)
            if register_user(username, password_hash, public_key):
                client_socket.send("Registration successful".encode('utf-8'))
            else:
                client_socket.send("Registration failed".encode('utf-8'))
        elif message.startswith("LOGIN"):
            _, username, password_hash = message.split(" ", 2)
            if validate_login(username, password_hash):
                public_key = get_public_key(username)
                response = f"Login successful {json.dumps(public_key)}"
                client_socket.send(response.encode('utf-8'))
            else:
                client_socket.send("Login failed".encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server(host='127.0.0.1', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
