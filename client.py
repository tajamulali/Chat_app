import socket

def register(username, password, client):
    client.send(f"REGISTER {username} {password}".encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    print(response)

def login(username, password, client):
    client.send(f"LOGIN {username} {password}".encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    if response == "Login successful":
        return True
    else:
        print(response)
        return False

def send_message(sender_username, receiver_username, message, client):
    client.send(f"SEND {sender_username} {receiver_username} {message}".encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    print(response)

def receive_messages(username, client):
    client.send(f"RECEIVE {username}".encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    print(response)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))

    while True:
        print("1. Register")
        print("2. Login")
        print("3. Send Message")
        print("4. Receive Messages")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register(username, password, client)

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if login(username, password, client):
                session_username = username

        elif choice == "3":
            if 'session_username' not in locals():
                print("You need to login first.")
                continue
            sender_username = session_username
            receiver_username = input("Enter receiver's username: ")
            message = input("Enter your message: ")
            send_message(sender_username, receiver_username, message, client)

        elif choice == "4":
            if 'session_username' not in locals():
                print("You need to login first.")
                continue
            username = session_username
            receive_messages(username, client)

        elif choice == "5":
            client.close()
            break

if __name__ == '__main__':
    main()
