from flask import Flask, jsonify, request, redirect
from shortURL import generate_short_id
from checkValid import is_valid_url

app = Flask(__name__)

url_db = {"12ihorvfkjab": "google.com",
  "ajkfkjabab": "pinterest.com",
  "fsuifbb": "facebook.com"
} #Need to store urls in CSV file instead

#we will create all RESTful endpoints here
#a repository of URLs - mapped to a short identifier
#GET: the keys 
#POST:  url to shorten and return id
#DELETE: not found

@app.route("/", methods = ["GET","POST","DELETE"])
def send_keys():
    if(request.method == 'GET'): 
        return jsonify(list(url_db.keys())), 200
    
    elif(request.method == 'POST'): 
        data = request.json
        if "url" not in data:
            return jsonify({"error": "Missing URL"}), 400
        
        url = data["url"]
        # Check if url is valid
        validity = is_valid_url(url)
        if validity == False:
            return jsonify({"error": "Invalid URL"}), 400
        short_id = generate_short_id(url)
        url_db[short_id] = url
        return jsonify({"short_id": short_id, "full_url": url}), 201

    else:
        return jsonify({"error": "DELETE on / is not allowed"}), 404

#call this api with(URL as input) 
#GET :get the url 
#PUT : put this id
#DELETE: delete the entry with this id

@app.route("/<string:id>", methods = ["GET","PUT","DELETE"])
def get_url(id):
    if(request.method == 'GET'): 
        if id in url_db:
            # return url_db([id])
            print("Entering GET")
            return jsonify(url_db[id]),301  # Redirect to full URL
        return jsonify({"error": "URL not found"}), 404
    
    elif(request.method == 'PUT'):
        data = request.json
        print(data)
        if "url" not in data:
            return jsonify({"error": "Missing URL"}), 400
        
        if id in url_db:
            url_db[id] = data["url"]  # Update existing entry
            return jsonify({"message": "URL updated"}), 200
        return jsonify({"error": "URL ID not found"}), 404

    else:
        if id in url_db:
            del url_db[id]
            return jsonify({"message": "deleted"}), 204 #some output issue here
        return jsonify({"error": "URL ID not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)