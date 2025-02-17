from flask import Flask, jsonify, request
from redis import Redis

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

    #do redis
    # check if username exists, check if old password matches to the one in database and then update with new password

@app.route("/users/login", methods=["POST"])
    def login():
        data = request.json
        if user and password: 
            return user,password
            generateJWT(user,password)
        else: 
            return jsonify({"Forbidden"}), 403
        # Check if username and password exist in the table and generate a JWT or else return 403

    #this function goes in url shortener service
    def authenticateUser():
        if authenticateUser:
            #manage their mappings 
        
        #present 
        #

    def generateJWT():
        #generate JSON
        #base64 encoding
        #sign it
        #if user authenticated 
        if authenticateUser()
            return JWT
        #Header
        header=  {
            'alg': 'HS256',
            'typ': 'JWT'
        }
        
        payload= {
            'sub': '1234567890',
            'name': 'John Doe',
            'admin': true
        }
        
    #sign it
    #The signature is used to verify that the sender of the JWT is who it says it is and to ensure that the message was’t changed in the way.
    signature =HMACSHA256(base64UrlEncode(header) + '.' + base64UrlEncode(payload), secret)
    #in url shortener we get JWT
    # use this JWT for authentication to validate the token and see if the user is login
if __name__ == '__main__':
    app.run(port=5001)