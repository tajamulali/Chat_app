import sqlite3
from hash import simple_hash

def create_user_table():
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            public_key TEXT NOT NULL
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
            sender TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password_hash, public_key):
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password, public_key) VALUES (?, ?, ?)', (username, password_hash, public_key))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_login(username, password):
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def save_message(sender, message):
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (sender, message) VALUES (?, ?)', (sender, message))
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('SELECT * FROM messages')
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
