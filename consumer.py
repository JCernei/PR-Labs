import queue
from flask import Flask, request
import time


consumer = Flask('consumer')

queue = queue.Queue(maxsize=10)


@consumer.get('/')
def hello_consumer():
    return 'hello, i am consumer'


@consumer.post('/consumer/receive/from/aggregator')
def consume():
    queue.put(int(request.form['value']))
    return 'ok'


def send_consumer_data(http):
    URL = 'http://127.0.0.1:8000/aggregator/receive/from/consumer'
    while True:
        value = queue.get()
        http.request('POST', URL, fields={
            'value': str(value).encode()})
        time.sleep(1)
