import sqlite3
from simple_hash import simple_hash

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('chat.db')
        print("Database connection established.")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL,
                           password_hash TEXT NOT NULL)''')
        conn.commit()
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def register_user(username, password):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            password_hash = simple_hash(password)
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
            print("User registered successfully.")
            return True
        except sqlite3.Error as e:
            print(f"Error registering user: {e}")
        finally:
            conn.close()
    return False

def validate_login(username, password):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            password_hash = simple_hash(password)
            cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
            user = cursor.fetchone()
            if user:
                print("Login successful.")
                return True
        except sqlite3.Error as e:
            print(f"Error validating login: {e}")
        finally:
            conn.close()
    print("Login failed.")
    return False
