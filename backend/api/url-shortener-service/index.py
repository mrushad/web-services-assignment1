from flask import Flask, jsonify, request
from redis import Redis
from shortURL import generate_short_id
from checkValid import is_valid_url

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

@app.route("/", methods=["GET", "POST", "DELETE"])
def send_keys():
    if request.method == 'GET':
        keys = [key.decode("utf-8") for key in redis.keys()]  # Decode keys from bytes
        return jsonify({"value": keys if keys else None}), 200
    
    elif request.method == 'POST':
        data = request.json
        if "value" not in data:
            return jsonify({"error": "Missing URL"}), 400
        
        url = data["value"]
        if not is_valid_url(url):
            return jsonify({"error": "Invalid URL"}), 400
        
        short_id = generate_short_id(url)
        redis.set(short_id, url)
        return jsonify({"id": short_id, "full_url": url}), 201

    else:
        redis.flushdb()
        return jsonify({"error": "Database cleared"}), 404

@app.route("/<id>", methods=["GET", "PUT", "DELETE"])
def get_url(id):
    if request.method == 'GET':
        url = redis.get(id)
        if url:
            return jsonify({"value": url.decode("utf-8")}), 301  # Redirect to full URL
        return jsonify({"error": "URL not found"}), 404
    
    elif request.method == 'PUT':
        data = request.get_json(force=True)
        if "url" not in data:
            return jsonify({"error": "Missing URL"}), 400
        
        if redis.exists(id):
            if is_valid_url(data["url"]):
                redis.set(id, data["url"])  # Update existing entry
                return jsonify({"message": "URL updated"}), 200
            return jsonify({"error": "Invalid URL"}), 400
        return jsonify({"error": "URL ID not found"}), 404
    

    else:
        if redis.exists(id):
            redis.delete(id)
            return jsonify({"message": "URL deleted"}), 204
        return jsonify({"error": "URL ID not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
