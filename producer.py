from flask import Flask, request
import random
import time

producer = Flask('producer')


@producer.get('/')
def hello_producer():
    return "hello, i am producer"


@producer.post('/producer/receive/from/aggregator')
def receive_data_back():
    print(int(request.form['value']))
    return 'received'


def send_producer_data(http):
    URL = 'http://127.0.0.1:8000/aggregator/receive/from/producer'
    while True:
        http.request('POST', URL, fields={
            'value': str(random.randint(0, 9)).encode()})
        time.sleep(1)
