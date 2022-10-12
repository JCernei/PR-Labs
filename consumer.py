import queue
from flask import Flask, request
import time


consumer = Flask('consumer')

queue = queue.Queue(maxsize=10)


@consumer.get('/')
def hello_consumer():
    return 'hello, i am consumer'


@consumer.post('/consume')
def consume():
    queue.put(int(request.form['value']))
    return 'ok'


def receive_and_send_data(http):
    URL = 'http://127.0.0.1:8080/receive'
    while True:
        value = queue.get()
        http.request('POST', URL, fields={
            'value': str(value).encode()})
        time.sleep(1)
