"""
Celery
======

This module houses a toy celery app for investigating Celery
"""
from tasks import add


SLEEP_TIME = 0.0001

def get_result(result):
    """Wait for the result of the task."""
    return result.get(timeout=1)


# result = add.delay(4, 4)
print("Starting Celery task")
print ("1 + 2 = ", get_result(add.delay(1, 2)))


