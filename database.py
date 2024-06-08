import sqlite3
from hash import simple_hash

def create_user_table():
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            public_key TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_message_table():
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return simple_hash(password)

def register_user(username, password):
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    try:
        hashed_password = hash_password(password)
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)

def validate_login(username, password):
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    if row:
        stored_password = row[0]
        return verify_password(stored_password, password)
    return False

def save_message(sender, message):
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (sender, message) VALUES (?, ?)', (sender, message))
    conn.commit()
    conn.close()

def get_messages(username):
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('SELECT * FROM messages WHERE sender = ?', (username,))
    messages = c.fetchall()
    conn.close()
    return messages

def store_public_key(username, public_key):
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('UPDATE users SET public_key = ? WHERE username = ?', (public_key, username))
    conn.commit()
    conn.close()

def get_public_key(username):
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('SELECT public_key FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None
