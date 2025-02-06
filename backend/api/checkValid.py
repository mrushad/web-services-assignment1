import re

# Your regex pattern
pattern = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?'

# Function to check URL validity
def is_valid_url(url):
    if re.match(pattern, url):
        return True
    else:
        return False