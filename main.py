import threading
import urllib3
from consumer import consumer, receive_and_send_data
from producer import producer, send_data


def run_producer():
    producer.run(host='127.0.0.1', port=8080)


def run_consumer():
    consumer.run(host='127.0.0.1', port=8081)


@producer.get('/start')
def start():
    for g in generators:
        g.start()
    for e in extractors:
        e.start()
    return 'start'


http = urllib3.PoolManager()

generators = [threading.Thread(target=send_data, args=(http,))
              for i in range(5)]
extractors = [threading.Thread(target=receive_and_send_data, args=(http,))
              for i in range(4)]


if __name__ == '__main__':
    t_producer = threading.Thread(target=run_producer)
    t_consumer = threading.Thread(target=run_consumer)
    t_producer.start()
    t_consumer.start()
