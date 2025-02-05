from flask import Flask, jsonify, request
app = Flask(__name__)


#we will create all RESTful endpoints here
#a repository of URLs - mapped to a short identifier

#GET: the keys 
#POST:  url to shorten and return id
#DELETE: not found

@app.route("/", methods = ["GET","POST","DELETE"])
def send_keys():
    if(request.method == 'GET'): 
        return "keys"
    elif(request.method == 'POST'): 
        # def shorten_url(url):
        return "id"
    else:
    # def delete_entry(url):
        return "404"

#call this api with(URL as input) 
#GET :get the url 
#PUT : put this id
#DELETE: delete the entry with this id

@app.route("/:id", methods = ["GET","PUT","DELETE"])
def get_url():
    if(request.method == 'GET'): 
            return "Send URL corresponding to the id"

    elif(request.method == 'PUT'):
        # def put_id(url, id):
        return "Update url and id"

    else:
        # def delete_url(id):
        return "Entry with {id} deleted"



