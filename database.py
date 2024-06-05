import sqlite3

def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash BLOB, public_key TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, sender_id INTEGER, receiver_id INTEGER, message TEXT, signature TEXT,
                  FOREIGN KEY(sender_id) REFERENCES users(id),
                  FOREIGN KEY(receiver_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

def register_user(username, password_hash, public_key):
    try:
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password_hash, public_key) VALUES (?, ?, ?)",
                  (username, password_hash, str(public_key)))
        conn.commit()
        conn.close()
        print("User registered successfully")  # Debugging print statement
    except sqlite3.Error as e:
        print("Error registering user:", e)  # Print error message


def get_user_by_username(username):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("SELECT id, password_hash, public_key FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def send_message(sender_id, receiver_id, message, signature):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (sender_id, receiver_id, message, signature) VALUES (?, ?, ?, ?)",
              (sender_id, receiver_id, message, str(signature)))
    conn.commit()
    conn.close()

def receive_messages(user_id):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("SELECT sender_id, message, signature FROM messages WHERE receiver_id=?", (user_id,))
    messages = c.fetchall()
    conn.close()
    return messages
