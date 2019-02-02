# To build the reverse module
# python setup.py build_ext --inplace
from __future__ import print_function
from reverse import is_palindrome as is_palindrome_cy
from time import time

ITERATAIONs = 1000

def is_palindrome_py(text):
    """ Return True is text is a palindrome, False otherwise"""
    for k, char in enumerate(reversed(text)):
        if text[k] != char:
            return False
    return True

def do_python(_cases):
    """ Return a list of times for testing palindromes on the given list"""
    print("Using python reversed")
    times = []
    for case in _cases:
        start = time()
        [is_palindrome_py(case) for k in range(ITERATAIONs)]
        times.append(time() - start)
    return times

def do_cython(_cases):
    """ Return a list of times for testing palindromes on the given list"""
    print("Using cython reversed")
    times = []
    for case in _cases:
        start = time()
        [is_palindrome_cy(case) for k in range(ITERATAIONs)]
        times.append(time() - start)
        
    return times

# Define the strings to be used. 
cases = ["b" * k for k in range(1000, 2000, 100)]
py_cases = do_python(cases)
cy_cases = do_cython(cases)
print("# Palindrome test for {0} iterations over a strings of length "
      "1000 to 2000".format(ITERATAIONs))
print("Python 1000 chars : ", py_cases[0])
print("Cython 1000 chars: ", cy_cases[0])
print("Python 2000 chars : ", py_cases[-1])
print("Cython 2000 chars: ", cy_cases[-1])
