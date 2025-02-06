import hashlib

def generate_short_id(url):
    return hashlib.md5(url.encode()).hexdigest()[:6]  # Take first 6 chars of MD5 hash

#could probably use a different hashing method