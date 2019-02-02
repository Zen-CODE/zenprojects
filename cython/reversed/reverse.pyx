# https://cython.readthedocs.io/en/latest/src/tutorial/strings.html

def is_palindrome(text):
    return bool(text == "".join(reversed(text)))

