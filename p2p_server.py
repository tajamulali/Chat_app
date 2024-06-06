import socket
import threading

class P2PServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []  # List to store peer connections
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"P2P Server started on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            self.peers.append(client_socket)
            threading.Thread(target=self.handle_peer, args=(client_socket,)).start()

    def handle_peer(self, client_socket):
        while True:
            try:
                # Handle peer communication here
                pass
            except Exception as e:
                print(f"Error handling peer: {str(e)}")
                self.peers.remove(client_socket)
                client_socket.close()

def main():
    p2p_server = P2PServer("0.0.0.0", 9999)
    p2p_server.start()

if __name__ == "__main__":
    main()
