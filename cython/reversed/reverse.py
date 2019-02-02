# To build the reverse module
# python setup.py build_ext --inplace
from reverse import is_palindrome as is_palindrome_cy

def is_palindrome_py(text):
    return bool(text == reversed(text))


cases = ["bob", "chop", "level"]

print("Using python reversed")
for case in cases:
    print(case, " is" if is_palindrome_py(case) else " not")

print("Using cython reversed")
for case in cases:
    print(case, " is" if is_palindrome_cy(case) else " not")

