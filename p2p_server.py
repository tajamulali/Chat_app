import socket
import threading
from database import create_user_table, create_message_table, register_user, validate_login, store_public_key, get_public_key

# Initialize the database tables
create_user_table()
create_message_table()

def handle_client(client_socket):
    try:
        message = client_socket.recv(1024).decode('utf-8')
        if message.startswith("REGISTER"):
            _, username, password, public_key = message.split(maxsplit=3)
            if register_user(username, password):
                store_public_key(username, public_key)
                client_socket.send("Registration successful".encode('utf-8'))
            else:
                client_socket.send("Registration failed".encode('utf-8'))
        elif message.startswith("LOGIN"):
            _, username, password = message.split(maxsplit=2)
            if validate_login(username, password):
                public_key = get_public_key(username)
                client_socket.send(f"Login successful {public_key}".encode('utf-8'))
            else:
                client_socket.send("Login failed".encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 9999))
    server_socket.listen(5)
    print("Server listening on 127.0.0.1:9999")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
