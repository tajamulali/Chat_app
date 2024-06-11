import socket
import threading
from database import register_user, validate_login

def handle_client(client_socket, addr):
    print(f"Accepted connection from {addr}")
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
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
            # Add more message handling logic here as needed
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()
        print(f"Connection closed with {addr}")

def start_peer(host='127.0.0.1', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Peer server started on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_peer()
