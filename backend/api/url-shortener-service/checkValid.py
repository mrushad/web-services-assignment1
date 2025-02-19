import re

'''
CREDITS:
Stack Overflow, “What is a good regular expression to
match a URL?” Stack Overflow, 2010. [Online]. Available:
https://stackoverflow.com/questions/3809401/what-is-a-good-regular-
expression-to-match-a-url
'''
pattern = r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'

# Function to check URL validity
def is_valid_url(url):
    if re.match(pattern, url):
        return True
    else:
        return False