import socket
import threading
import json
from database import create_user_table, create_message_table, register_user, validate_login, save_message, get_messages, get_public_key
from hash import simple_hash
from rsa import generate_keys, sign_message, verify_signature

# Initialize the database tables
create_user_table()
create_message_table()

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.peers = {}
        self.username = None
        self.public_key, self.private_key = generate_keys()
        self.peer_public_keys = {}
        print(f"Peer started on {self.host}:{self.port}")

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=self.handle_connection, args=(client_socket,)).start()

    def handle_connection(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    signed_message = json.loads(message)
                    received_message = signed_message.get('message')
                    signature = signed_message.get('signature')
                    username = signed_message.get('username')
                    if username not in self.peer_public_keys:
                        self.peer_public_keys[username] = json.loads(get_public_key(username))
                    if username in self.peer_public_keys and verify_signature(self.peer_public_keys[username], received_message, signature):
                        print(f"Received message from {username}: {received_message}")
                        save_message(username, received_message)
                    else:
                        print("Invalid signature or unknown user")
                else:
                    client_socket.close()
                    break
            except Exception as e:
                print(f"Error handling connection: {e}")
                client_socket.close()
                break

    def register(self, username, password, server_address):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(server_address)
            public_key_str = json.dumps(self.public_key)
            client_socket.send(f"REGISTER {username} {password} {public_key_str}".encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(response)
            return response == "Registration successful"

    def login(self, username, password, server_address):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(server_address)
            client_socket.send(f"LOGIN {username} {password}".encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(response)
            if response.startswith("Login successful"):
                self.username = username
                public_key_str = response.split(" ", 2)[2]
                self.peer_public_keys[username] = json.loads(public_key_str)
                return True
            return False

    def send_message(self, peer_address, message):
        if self.username:
            signed_message = {
                'username': self.username,
                'message': message,
                'signature': sign_message(self.private_key, message)
            }
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer_socket:
                peer_socket.connect(peer_address)
                peer_socket.send(json.dumps(signed_message).encode('utf-8'))

def main():
    peer_host = input("Enter peer host (e.g., 127.0.0.1): ")
    peer_port = int(input("Enter peer port (e.g., 8888): "))

    peer = Peer(peer_host, peer_port)

    while True:
        print("1. Register")
        print("2. Login")
        print("3. Send Message")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if peer.register(username, password, ("127.0.0.1", 9999)):
                print("Registration successful")
            else:
                print("Registration failed")
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if peer.login(username, password, ("127.0.0.1", 9999)):
                print("Login successful")
                threading.Thread(target=peer.start).start()  # Start listening for incoming connections
            else:
                print("Login failed")
        elif choice == "3":
            peer_host = input("Enter peer host to send message to: ")
            peer_port = int(input("Enter peer port to send message to: "))
            message = input("Enter message: ")
            peer.send_message((peer_host, peer_port), message)
        elif choice == "4":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
