import socket
import threading

class Peer:
    def __init__(self, username, host, port):
        self.username = username
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Peer {self.username} started on {self.host}:{self.port}")

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

def main():
    username = input("Enter your username: ")
    peer = Peer(username, "0.0.0.0", 8888)  # Use different ports for different peers
    peer.start()

if __name__ == "__main__":
    main()
