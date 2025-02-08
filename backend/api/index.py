from flask import Flask, jsonify, request, redirect
from .shortURL import generate_short_id
from .checkValid import is_valid_url

app = Flask(__name__)

url_db = {} #a repository of URLs - mapped to a short identifier

#we will create all RESTful endpoints here
#GET: the keys 
#POST:  url to shorten and return id
#DELETE: not found

@app.route("/", methods = ["GET","POST","DELETE"])
def send_keys():
    if(request.method == 'GET'): 
        return jsonify({"value" : list(url_db.keys()) if url_db.keys() else None}), 200
    
    elif(request.method == 'POST'): 
        data = request.json
        if "value" not in data:
            return jsonify({"error": "Missing URL"}), 400
        
        url = data["value"]
        # Check if url is valid
        validity = is_valid_url(url)
        if validity == False:
            return jsonify({"error": "Invalid URL"}), 400
        short_id = generate_short_id(url)
        url_db[short_id] = url
        return jsonify({"id": short_id, "full_url": url}), 201

    else:
        url_db.clear()
        return jsonify({"error": "Database cleared"}), 404

#call this api with(URL as input) 
#GET :get the url 
#PUT : put this id
#DELETE: delete the entry with this id

@app.route("/<id>", methods = ["GET","PUT","DELETE"])
def get_url(id):
    if(request.method == 'GET'): 
        if id in url_db:
            return jsonify({"value":url_db[id]}), 301  # Redirect to full URL
        return jsonify({"error": "URL not found"}), 404
    
    elif(request.method == 'PUT'):
        data = request.json
        if "value" not in data: #also need to check if the new URL is valid
            return jsonify({"error": "Missing URL"}), 400
        
        if id in url_db:
            url_db[id] = data["value"]  # Update existing entry
            return jsonify({"message": "URL updated"}), 200
        return jsonify({"error": "URL ID not found"}), 404

    else:
        if id in url_db:
            del url_db[id]
            return jsonify({"message": "URL deleted"}), 204 
        return jsonify({"error": "URL ID not found"}), 404

if __name__ == '__main__':
    app.run(debug = True)