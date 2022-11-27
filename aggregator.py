import queue
from flask import Flask, request
import time
import random

aggregator = Flask('aggregator')

producer_queue = queue.Queue(maxsize=10)
consumer_queue = queue.Queue(maxsize=10)


@aggregator.get('/')
def hello_aggregator():
    return 'hello, i am aggregator'


@aggregator.post('/aggregator/receive/from/consumer')
def consume():
    consumer_queue.put(int(request.form['value']))
    return 'ok'


@aggregator.post('/aggregator/receive/from/producer')
def receive_data_back():
    producer_queue.put(int(request.form['value']))
    return 'received'


def send_consumer_aggregated_data(http):
    URL = 'http://127.0.0.1:8080/producer/receive/from/aggregator'
    while True:
        value = consumer_queue.get()
        http.request('POST', URL, fields={
            'value': str(value).encode()})
        time.sleep(1)


def send_producer_aggregated_data(http):
    URL = 'http://127.0.0.1:8081/consumer/receive/from/aggregator'
    while True:
        value = producer_queue.get()
        http.request('POST', URL, fields={
            'value': str(value).encode()})
        time.sleep(1)
