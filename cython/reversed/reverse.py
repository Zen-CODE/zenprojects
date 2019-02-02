# To build the reverse module
# python setup.py build_ext --inplace
from __future__ import print_function
from reverse import is_palindrome as is_palindrome_cy

def is_palindrome_py(text):
    for k, char in enumerate(reversed(text)):
        if text[k] != char:
            return False
    return True


cases = ["bob", "chop", "level"]
for k in range(2, 11):
    cases += [itm * k for itm in cases]

def do_python():
    print("Using python reversed")
    for case in cases:
        print(" is" if is_palindrome_py(case) else " not", end='')
    print('')

def do_cython():
    print("Using cython reversed")
    for case in cases:
        print(" is" if is_palindrome_cy(case) else " not", end='')
    print('')


do_python()
do_cython()