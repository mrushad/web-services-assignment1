from flask import Flask, jsonify, request
from redis import Redis
from shortURL import generate_short_id
from checkValid import is_valid_url
import logging
import requests
app = Flask(__name__)

# Initialize Redis connection
redis = Redis(host='localhost', port=6379, db=0)


#assignment 2

"""
1.Multi-user support. 
2.Authentication service: database of users used to login. Send out JWTs
3. URL shortner -> Users required to authenticate, associate mappings and permissions
4. User-> send the JWT to your shortener service authentication service 
validate the token and see if the user is actually logged in
"""

#for every function we need to check if the user is authenticated/ JWT matches?
#communicate with the auth_service api to get the JWT of a user
#validate the token to see if the user is actually logged in


AUTH_SERVICE_URL = 'http://localhost:5001'

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def authenticate_request():
    token = request.headers.get('Authorization')
    if not token:
        logging.debug("No token provided")
        return None
    
    response = requests.post(f'{AUTH_SERVICE_URL}/verify', json={'token': token})
    logging.debug(f"Authentication service response: {response.status_code}, {response.content}")
    if response.status_code == 200:
        return response.json()['username']
    return None

@app.route("/", methods=["GET", "POST", "DELETE"])
def send_keys():
    username = authenticate_request()
    if not username:
        return jsonify({"error": "forbidden"}), 403
    
    if request.method == 'GET':
        keys = [key.decode("utf-8") for key in redis.keys(f'{username}:*')]  # Decode keys from bytes
        if not keys:
            return jsonify({"error": "No entries found"}), 404
        return jsonify({"value": keys}), 200
    
    elif request.method == 'POST':
        data = request.json
        if "value" not in data:
            return jsonify({"error": "Missing URL"}), 400
        
        url = data["value"]
        if not is_valid_url(url):
            return jsonify({"error": "Invalid URL"}), 400
        
        short_id = generate_short_id(url)
        redis.set(f'{username}:{short_id}', url)
        return jsonify({"id": short_id, "full_url": url}), 201

    else:
        keys = redis.keys(f'{username}:*')
        if not keys:
            return jsonify({"error": "No entries to delete"}), 404
        redis.delete(*keys)
        ### CHECK ERROR CODE FOR ABOVE NO ENTRIES TO DELETE
        return jsonify({"message": "Database cleared"}), 404

@app.route("/<id>", methods=["GET", "PUT", "DELETE"])
def get_url(id):
    username = authenticate_request()
    if not username:
        return jsonify({"error": "forbidden"}), 403
    
    key = f'{username}:{id}'
    if request.method == 'GET':
        url = redis.get(key)
        if url:
            return jsonify({"value": url.decode("utf-8")}), 301  # Redirect to full URL
        return jsonify({"error": "URL not found"}), 404
    
    elif request.method == 'PUT':
        data = request.get_json(force=True)
        if "url" not in data:
            return jsonify({"error": "Missing URL"}), 400
        
        if redis.exists(key):
            if is_valid_url(data["url"]):
                redis.set(key, data["url"])  # Update existing entry
                return jsonify({"message": "URL updated"}), 200
            return jsonify({"error": "Invalid URL"}), 400
        return jsonify({"error": "URL ID not found"}), 404

    else:
        if redis.exists(key):
            redis.delete(key)
            return jsonify({"message": "URL deleted"}), 204
        return jsonify({"error": "URL ID not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)