from celery import Celery

app = Celery('qqqq', broker='amqp://localhost')

@app.task
def add(x, y):
    return x + y
