"""
This module implements a optimized 'is_palindrom' function using cython
memoryviews to avoid overhead of iterating over the reversed sting in python
"""
# https://cython.readthedocs.io/en/latest/src/userguide/memoryviews.html

def is_palindrome(const unsigned char[:] text):
    cdef int k
    cdef int length = text.shape[0]

    for k in range(0, length / 2):
        if text[k] !=  text[length - k - 1]:
            return False
    return True

