import re

# Your regex pattern
pattern = r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'

# Function to check URL validity
def is_valid_url(url):
    if re.match(pattern, url):
        return True
    else:
        return False