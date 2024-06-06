import socket
import threading

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Peer started on {self.host}:{self.port}")

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=self.handle_connection, args=(client_socket,)).start()

    def handle_connection(self, client_socket):
        while True:
            try:
                # Handle peer-to-peer communication here
                pass
            except Exception as e:
                print(f"Error handling connection: {str(e)}")
                client_socket.close()
                break

    def register(self, username, password, server_address):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(server_address)
            client_socket.send(f"REGISTER {username} {password}".encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(response)

    def login(self, username, password, server_address):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(server_address)
            client_socket.send(f"LOGIN {username} {password}".encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(response)
            return response == "Login successful"

def main():
    host = "127.0.0.1"
    port = 8888
    server_address = ("127.0.0.1", 9999)

    peer = Peer(host, port)

    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            peer.register(username, password, server_address)

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if peer.login(username, password, server_address):
                print("Login successful! You can now send and receive messages.")
                # After login, start the peer server to accept connections
                threading.Thread(target=peer.start).start()
                break

        elif choice == "3":
            break

if __name__ == "__main__":
    main()
