# goshawk-python

Python library for writing Goshawk agents, reporters and subscribers.

## Install

```
pip install git+https://github.com/lukasic/goshawk-python
```

## Usage

### Goshawk API client

Client for communicating with Goshawk via REST API.

```python
from goshawk.client import GoshawkClient

goshawk = GoshawkClient("https://goshawk-api/api/")

blocklist_ip = goshawk.get_records_values(list_name="mylist")

```

### Reporter classes

**goshawk.reporter.WorkerPool** can be used for paralelization and managing multiple workers.

**goshawk.reporter.RabbitmqConsumer** is wrapper class for subscribing AMQP queue.

```python
queue = list()

is_running = True
def worker(id):
    while is_running:
        # not thread safe
        data = queue.pop()
        process(data)

def callback(ch, method, properties, body):
    data = body.decode()
    queue.append(data)

workers = WorkerPool(target=worker, threads=4)
workers.start()

rmqconsumer = RabbitmqConsumer(
    amqp_uri, exchange, routing_key, consumer_name_prefix)

rmqconsumer.consume(callback=callback)

is_running = False
workers.join()
```
