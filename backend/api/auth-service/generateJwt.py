import base64
import hmac
import hashlib
import json
import os
import datetime

'''
TODO
- ADD REFERENCES/CREDITS IN CODE
- VERIFY TOKEN GENERATION WITH POSTMAN
'''

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

def generate_jwt(username, secret):
    header = {
        'alg': 'HS256',            
        'typ': 'JWT'
    }
            
    payload = {
        'username': username,
        'exp': (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).timestamp()
    }
            
    encoded_header = base64url_encode(json.dumps(header).encode("utf-8"))
    encoded_payload = base64url_encode(json.dumps(payload).encode("utf-8"))
        
    message = f"{encoded_header}.{encoded_payload}"
    signature = base64url_encode(hmac_sha256(secret, message))

    jwt_token = f"{message}.{signature}"
    return jwt_token

def verify_jwt(token, secret):
    try:
        encoded_header, encoded_payload, signature = token.split('.')
        message = f"{encoded_header}.{encoded_payload}"
        expected_signature = base64url_encode(hmac_sha256(secret, message))
        
        if signature != expected_signature:
            return None
        
        payload = json.loads(base64.urlsafe_b64decode(encoded_payload + '==').decode('utf-8'))
        if datetime.datetime.utcnow().timestamp() > payload['exp']:
            return None
        
        return payload['username']
    except Exception as e:
        return None