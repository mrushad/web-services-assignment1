from flask import Flask, request, jsonify
import hashlib
import logging
from generateJwt import generate_jwt, verify_jwt, generate_secret
from redis import Redis

app = Flask(__name__)

# Initialize Redis connection
redis = Redis(host='redis', port=6379, db=0)

# Calling generate_secret function to generate a random secret
app.config['SECRET_KEY'] = '29ac8931f285b1e0cb75438a'

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Hashing the password to sha256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Route to create user 
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if redis.exists(f'user:{username}'):
        return jsonify({"error": "duplicate"}), 409
    
    redis.set(f'user:{username}', hash_password(password))
    return jsonify({"message": "User created"}), 201

# Route to update user's password
@app.route('/users', methods=['PUT'])
def update_password():
    data = request.json
    username = data.get('username')
    old_password = data.get('old-password')
    new_password = data.get('new-password')
    
    if not redis.exists(f'user:{username}') or redis.get(f'user:{username}').decode('utf-8') != hash_password(old_password):
        return jsonify({"error": "forbidden"}), 403
    
    redis.set(f'user:{username}', hash_password(new_password))
    return jsonify({"message": "Password updated"}), 200

# Route for user login
@app.route('/users/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not redis.exists(f'user:{username}') or redis.get(f'user:{username}').decode('utf-8') != hash_password(password):
        logging.debug(f"Login failed for user: {username}")
        return jsonify({"error": "forbidden"}), 403
    # Generate token using the username and secret key
    token = generate_jwt(username, app.config['SECRET_KEY'])
    logging.debug(f"Login successful for user: {username}, token: {token}")
    return jsonify({"token": token}), 200

# Verify route
@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    token = data.get('token')
    username = verify_jwt(token, app.config['SECRET_KEY'])
    if username:
        return jsonify({"username": username}), 200
    return jsonify({"error": "forbidden"}), 403

# Logout route
@app.route('/users/logout', methods=['POST'])
def logout():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing token"}), 400
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]
    username = verify_jwt(token, app.config['SECRET_KEY'])

    redis.sadd('revoked_tokens', token)  # Store revoked token

    if username and redis.sismember('revoked_tokens', token):
        redis.srem('revoked_tokens', username)
        logging.debug(f"Token Revoked: {token}")
        logging.debug(f"Logging out user: {username}")

    return jsonify({"message": "Logged out successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
