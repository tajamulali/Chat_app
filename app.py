from flask import Flask, request, jsonify
import sqlite3
import hashlib
import os
from rsa_utils import generate_rsa_keypair, rsa_sign, rsa_verify

app = Flask(__name__)
DATABASE = 'chatapp.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    
    # Hash the password with a salt
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    
    # Generate RSA keys
    (public_key, private_key) = generate_rsa_keypair(2048)
    
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash, public_key) VALUES (?, ?, ?)', 
                           (username, salt + password_hash, str(public_key)))
            conn.commit()
            return jsonify({'private_key': str(private_key)}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

@app.route('/send', methods=['POST'])
def send_message():
    sender_id = request.json['sender_id']
    receiver_id = request.json['receiver_id']
    message = request.json['message']
    private_key = eval(request.json['private_key'])  # Converting string back to tuple
    
    # Create message hash
    message_hash = hashlib.sha256(message.encode()).digest()
    
    # Sign the message hash
    signature = rsa_sign(message_hash, private_key)
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (sender_id, receiver_id, message, signature) VALUES (?, ?, ?, ?)', 
                       (sender_id, receiver_id, message, signature))
        conn.commit()

    return jsonify({'status': 'Message sent'}), 200

@app.route('/receive', methods=['POST'])
def receive_message():
    message_id = request.json['message_id']
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT sender_id, message, signature FROM messages WHERE id = ?', (message_id,))
        row = cursor.fetchone()

    sender_id, message, signature = row
    
    cursor.execute('SELECT public_key FROM users WHERE id = ?', (sender_id,))
    sender_public_key = eval(cursor.fetchone()[0])  # Converting string back to tuple
    
    message_hash = hashlib.sha256(message.encode()).digest()
    
    if rsa_verify(message_hash, signature, sender_public_key):
        return jsonify({'message': message, 'status': 'Verified'}), 200
    else:
        return jsonify({'error': 'Signature verification failed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
