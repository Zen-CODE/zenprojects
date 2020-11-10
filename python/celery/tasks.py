from celery import Celery
from time import sleep

app = Celery('tasks', backend='redis://localhost',
             broker='redis://guest@localhost//')


@app.task
def add(x, y):
    print("Sleeping...")
    sleep(10.0)
    return x + y
