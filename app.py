from rsa_utils import generate_key_pair, sign_message, verify_message
from auth_utils import hash_password, verify_password
from database import init_db, register_user, get_user_by_username, send_message, receive_messages

def register(username, password):
    public_key, private_key = generate_key_pair()
    hashed_password = hash_password(password)
    register_user(username, hashed_password, public_key)
    return private_key

def login(username, password):
    user = get_user_by_username(username)
    if user and verify_password(user[1], password):
        return user[0], eval(user[2])  # Returning user ID and public key
    return None, None

def main():
    init_db()

    print("Chat Application")
    while True:
        action = input("Do you want to (register/login/exit): ").strip().lower()
        if action == 'register':
            username = input("Enter username: ")
            password = input("Enter password: ")
            private_key = register(username, password)
            print(f"User {username} registered successfully. Keep your private key safe.")
            print(f"Private Key: {private_key}")

        elif action == 'login':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_id, public_key = login(username, password)
            if user_id:
                print(f"Welcome, {username}!")
                while True:
                    command = input("Do you want to (send/receive/logout): ").strip().lower()
                    if command == 'send':
                        receiver = input("Enter receiver's username: ")
                        receiver_user = get_user_by_username(receiver)
                        if receiver_user:
                            message = input("Enter your message: ")
                            signature = sign_message(private_key, message)
                            send_message(user_id, receiver_user[0], message, signature)
                            print("Message sent!")
                        else:
                            print("Receiver not found.")
                    elif command == 'receive':
                        messages = receive_messages(user_id)
                        for sender_id, message, signature in messages:
                            sender_user = get_user_by_username(sender_id)
                            is_valid = verify_message(eval(sender_user[2]), message, int(signature))
                            print(f"Message from {sender_user[0]}: {message}, Signature valid: {is_valid}")
                    elif command == 'logout':
                        break
                    else:
                        print("Invalid command.")
            else:
                print("Invalid username or password.")

        elif action == 'exit':
            break

        else:
            print("Invalid action.")

if __name__ == '__main__':
    main()
