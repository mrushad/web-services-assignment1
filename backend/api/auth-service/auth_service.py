from flask import Flask, request, jsonify
import hashlib
import jwt
import datetime
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_generated_secret_key'

# Configure logging
logging.basicConfig(level=logging.DEBUG)

users = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username in users:
        return jsonify({"error": "duplicate"}), 409
    
    users[username] = hash_password(password)
    return jsonify({"message": "User created"}), 201

@app.route('/users', methods=['PUT'])
def update_password():
    data = request.json
    username = data.get('username')
    old_password = data.get('old-password')
    new_password = data.get('new-password')
    
    if username not in users or users[username] != hash_password(old_password):
        return jsonify({"error": "forbidden"}), 403
    
    users[username] = hash_password(new_password)
    return jsonify({"message": "Password updated"}), 200

@app.route('/users/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username not in users or users[username] != hash_password(password):
        logging.debug(f"Login failed for user: {username}")
        return jsonify({"error": "forbidden"}), 403
    
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    logging.debug(f"Login successful for user: {username}, token: {token}")
    return jsonify({"token": token}), 200

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    token = data.get('token')
    username = verify_token(token)
    if username:
        return jsonify({"username": username}), 200
    return jsonify({"error": "forbidden"}), 403

def verify_token(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return data['username']
    except Exception as e:
        logging.debug(f"Token verification failed: {e}")
        return None

if __name__ == '__main__':
    app.run(port=5001, debug=True)