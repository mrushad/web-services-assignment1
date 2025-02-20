from flask import Flask, request, jsonify
import hashlib
import logging
from generateJwt import generate_jwt, verify_jwt, generate_secret

app = Flask(__name__)
app.config['SECRET_KEY'] = generate_secret()


# Configure logging
logging.basicConfig(level=logging.DEBUG)

users = {}
revoked_tokens = {}
'''
TODO
- ADD REFERENCES AND CREDITS
- CHANGE SECRET_KEY
- VERIFY ERROR CODES MATCH REQUIREMENT SPECIFICATION
- VERIFY SECRET KEY IS NOT SHARED WITH URL SERVICE
- 

'''
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
    
    token = generate_jwt(username, app.config['SECRET_KEY'])
    logging.debug(f"Login successful for user: {username}, token: {token}")
    return jsonify({"token": token}), 200
@app.route('/users/logout', methods=['POST'])
def logout():
    # data = request.json
    
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing token"}), 400
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]
    username = verify_jwt(token, app.config['SECRET_KEY'])

    revoked_tokens.add(token)  # Store revoked token

    if username and username in revoked_tokens:
        del revoked_tokens[username]
        print("logged out")
    logging.debug(f"Token Revoked: {token}")
    
    
    logging.debug(f"Logging out user: {username}")

    return jsonify({"message": "Logged out successfully"}), 200
    
@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    token = data.get('token')
    username = verify_jwt(token, app.config['SECRET_KEY'])
    if username:
        return jsonify({"username": username}), 200
    return jsonify({"error": "forbidden"}), 403

if __name__ == '__main__':
    app.run(port=5001, debug=True)