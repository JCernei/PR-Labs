import threading
import urllib3
from consumer import consumer, send_consumer_data
from producer import producer, send_producer_data
from aggregator import aggregator, send_consumer_aggregated_data, send_producer_aggregated_data


def run_producer():
    producer.run(host='127.0.0.1', port=8080)


def run_aggregator():
    aggregator.run(host='127.0.0.1', port=8000)


def run_consumer():
    consumer.run(host='127.0.0.1', port=8081)


@producer.get('/start')
def start():
    for g in generators:
        g.start()
    for ag in aggregator_generators:
        ag.start()
    for ae in aggregator_extractors:
        ae.start()
    for e in extractors:
        e.start()
    return 'start'


http = urllib3.PoolManager()

generators = [threading.Thread(target=send_producer_data, args=(http,))
              for i in range(10)]

aggregator_generators = [threading.Thread(target=send_producer_aggregated_data, args=(http,))
                         for i in range(10)]
aggregator_extractors = [threading.Thread(target=send_consumer_aggregated_data, args=(http,))
                         for i in range(7)]

extractors = [threading.Thread(target=send_consumer_data, args=(http,))
              for i in range(7)]


if __name__ == '__main__':
    t_producer = threading.Thread(target=run_producer)
    t_aggregator = threading.Thread(target=run_aggregator)
    t_consumer = threading.Thread(target=run_consumer)
    t_producer.start()
    t_aggregator.start()
    t_consumer.start()
