import sqlite3
import hashlib
from rsa import generate_rsa_keys, sign_rsa, verify_rsa

def setup_db():
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            public_key_n TEXT,
            public_key_e TEXT,
            private_key_d TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            message TEXT,
            signature TEXT,
            FOREIGN KEY(sender_id) REFERENCES users(id),
            FOREIGN KEY(receiver_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    password_hash = hash_password(password)
    public_key, private_key = generate_rsa_keys()
    public_key_e, public_key_n = public_key
    private_key_d, _ = private_key

    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password_hash, public_key_n, public_key_e, private_key_d) VALUES (?, ?, ?, ?, ?)',
                  (username, password_hash, str(public_key_n), str(public_key_e), str(private_key_d)))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def get_user(username):
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def validate_login(username, password):
    password_hash = hash_password(password)
    user = get_user(username)
    if user and user[2] == password_hash:
        return True
    return False

def send_message(sender_username, receiver_username, message):
    sender = get_user(sender_username)
    receiver = get_user(receiver_username)
    if not sender or not receiver:
        return False

    private_key = (int(sender[5]), int(sender[3]))
    signature = sign_rsa(private_key, message)

    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (sender_id, receiver_id, message, signature) VALUES (?, ?, ?, ?)',
              (sender[0], receiver[0], message, str(signature)))
    conn.commit()
    conn.close()
    return True

def receive_messages(username):
    user = get_user(username)
    if not user:
        return []

    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('SELECT messages.message, messages.signature, users.public_key_n, users.public_key_e FROM messages '
              'JOIN users ON messages.sender_id = users.id '
              'WHERE messages.receiver_id = ?', (user[0],))
    messages = c.fetchall()
    conn.close()

    verified_messages = []
    for message, signature, public_key_n, public_key_e in messages:
        public_key = (int(public_key_e), int(public_key_n))
        if verify_rsa(public_key, message, int(signature)):
            verified_messages.append(message)

    return verified_messages
