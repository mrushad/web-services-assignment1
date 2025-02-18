from flask import Flask, jsonify, request
from redis import Redis

from generateJwt import generateJWT

#Authentication service: database of users used to login. Send out JWTs
app = Flask(__name__)

# Initialize Redis connection
redis = Redis(host='localhost', port=6380, db=0)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    #create query
    if redis.exists(data["username"]):
        return jsonify({"error": "Username already exists"}), 409
    else:
        redis.set(data["username"], data["password"])
        return jsonify({"message": "New user created!"}), 200
    
@app.route("/users", methods=["PUT"])
def update_password():
    data = request.json
    if(data["password"]==redis("password")):
        redis.update["password"]= data("new_password")
        return jsonify({"message": "Password updated!"}), 200
    else:
        return jsonify({"message":"Forbidden"}), 403
    #do redis
    # check if username exists, check if old password matches to the one in database and then update with new password

@app.route("/users/login", methods=["POST"])
def login():
    data = request.json
    if redis.exists(data["username"]) and redis.exists(data["password"]):
        return generateJWT(data), 200
    else: 
        return jsonify({"message Forbidden"}), 403
        # Check if username and password exist in the table and generate a JWT or else return 403
    
    # use this JWT for authentication to validate the token and see if the user is login
if __name__ == '__main__':
    app.run(port=5001)