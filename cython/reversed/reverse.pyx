# https://cython.readthedocs.io/en/latest/src/tutorial/strings.html

def is_palindrome(const unsigned char[:] text):
    cdef int k
    cdef int length = text.shape[0]

    for k in range(0, length / 2):
        if text[k] !=  text[length - k - 1]:
            return False
    return True

