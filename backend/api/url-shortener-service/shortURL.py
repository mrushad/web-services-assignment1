import hashlib

def generate_hash5(url):
    return hashlib.md5(url.encode()).hexdigest()[:6]   #Take first 6 chars of MD5 hash

#hash it first -> convert it to decimal ->
base62Digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def convert_base62(num): 
    # base62digits = generate_hash5(url) #ajhfb1
    base62 = ""
    while num>0: 
        r = num%62 #remainder
        base62 = str(base62Digits[int(r)]) + base62
        num = num/62
    return base62[-4:]

def generate_short_id(url):
    string = generate_hash5(url) #a137b
    num = int(string, 16) 
    return convert_base62(num)
