import sqlite3
import hashlib

def setup_db():
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    password_hash = hash_password(password)

    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
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
