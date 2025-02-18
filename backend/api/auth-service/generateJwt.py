import base64, hmac, hashlib, json, os

#this function goes in url shortener service
def base64url_encode(data):
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip("=")
    
def hmac_sha256(key, message):
        return hmac.new(
            key.encode("utf-8"),
            message.encode("utf-8"), 
            hashlib.sha256
        ).digest()
def generate_secret():
    """Generates a secure random secret for HMAC."""
    # Generate a 256-bit random secret (32 bytes)
    secret = os.urandom(32)
    # Encode it in base64 to get a URL-safe string
    return base64.urlsafe_b64encode(secret).decode('utf-8').rstrip("=")
def generateJWT():
        # generate JSON
        # base64 encoding
        # sign it
        # if user authenticated 
        
        # Header
    header=  {
        'alg': 'HS256',            
        'typ': 'JWT'
    }
            
    payload= {
        'sub': '1234567890',
        'name': 'John Doe',
        'admin': True
    }
            
        #encoding JSON 
    encoded_header = base64url_encode(json.dumps(header).encode("utf-8"))
    encoded_payload = base64url_encode(json.dumps(payload).encode("utf-8"))
        
        #concatenate 
    message = f"{encoded_header}.{encoded_payload}"

        #sign it
        #The signature is used to verify that the sender of the JWT is who it says it is and to ensure that the message was’t changed in the way.
    secret = generate_secret()
    signature = base64url_encode(hmac_sha256(secret, message))
        #in url shortener we get JWT

    jwt_token = f"{message}.{signature}"
    return jwt_token
print(generateJWT()) 

