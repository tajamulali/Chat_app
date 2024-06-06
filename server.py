import socket
import threading
from database import setup_db, register_user, validate_login, send_message, receive_messages

def handle_client(client_socket):
    while True:
        try:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break

            command, *args = request
            command, *args = request.split()
            response = "Invalid command"

            if command == "REGISTER":
                username, password = args
                if register_user(username, password):
                    response = "Registration successful"
                else:
                    response = "Username already exists"

            elif command == "LOGIN":
                username, password = args
                if validate_login(username, password):
                    response = "Login successful"
                else:
                    response = "Invalid credentials"

            elif command == "SEND":
                sender_username, receiver_username, message = args
                if send_message(sender_username, receiver_username, message):
                    response = "Message sent"
                else:
                    response = "Failed to send message"

            elif command == "RECEIVE":
                username = args[0]
                messages = receive_messages(username)
                response = "\n".join(messages) if messages else "No messages"

            client_socket.send(response.encode('utf-8'))

        except Exception as e:
            client_socket.send(f"Error: {str(e)}".encode('utf-8'))
            break

    client_socket.close()

def main():
    setup_db()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server started on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()
