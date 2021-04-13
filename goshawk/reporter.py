import pika
import uuid
import signal
import threading

class RabbitmqConsumer:

    def __init__(self, amqp_uri, exchange, routing_key, consumer_name_prefix):
        self.stop_consuming = False

        self.queue = consumer_name_prefix + "-" + str(uuid.uuid4())[:10]

        self.params = pika.URLParameters(amqp_uri)
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        
        self.channel.queue_declare(
            queue=self.queue,
            exclusive=True)
        
        self.channel.queue_bind(
            queue=self.queue,
            exchange=exchange,
            routing_key=routing_key)

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def consume(self, callback):
        #self.logger.debug("Starting consuming...")
        self.connection.call_later(0.1, self.check_stop)
        self.channel.basic_consume(
            self.queue,
            callback,
            exclusive=True,
            auto_ack=True)
        
        self.channel.start_consuming()
        #self.logger.debug("Consuming finished.")

    def stop(self, signal, frame):
        print("Caught signal. Stopping rabbitmq consumer...")
        self.stop_consuming = True

    def check_stop(self):
        if self.stop_consuming:
            self.channel.stop_consuming()
        self.connection.call_later(0.1, self.check_stop)

    def signal_handler(signal, frame):
        global stop_consuming
        self.stop_consuming = True

    def stop_signal(self, signal):
        signal.signal(signal, self.stop)


class WorkerPool:
    def __init__(self, target, threads=4):
        self.thr_list = dict()
        self.is_running = True
        self.threads_count = threads
        self.target = target

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop(self):
        print("Caught signal. Stopping workers...")
        self.is_running = False

    def start(self):
        for i in range(self.threads_count):
            print("Starting worker %d" % i)
            self.thr_list[i] = threading.Thread(target=self.target, args={ i })
            self.thr_list[i].start()

    def join(self):
        for i in self.thr_list.keys():
            self.thr_list[i].join()
