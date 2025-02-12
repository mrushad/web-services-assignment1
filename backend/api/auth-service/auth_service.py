from flask import Flask, jsonify, request
from redis import Redis

app = Flask(__name__)

# Initialize Redis connection
redis = Redis(host='localhost', port=6380, db=0)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if redis.exists(data["username"]):
        return jsonify({"error": "Username already exists"}), 409
    else:
        redis.set(data["username"], data["password"])
        return jsonify({"message": "New user created!"}), 200
    
@app.route("/users", methods=["PUT"])
def update_password():
    data = request.json
    # check if username exists, check if old password matches to the one in database and then update with new password

@app.route("/users/login", methods=["POST"])
def login():
    data = request.json
    # Check if username and password exist in the table and generate a JWT or else return 403


if __name__ == '__main__':
    app.run(port=5001)