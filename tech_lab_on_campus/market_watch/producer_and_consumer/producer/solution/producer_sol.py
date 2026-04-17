import pika
from concurrent.futures import ThreadPoolExecutor
from interfaces.producerInterface import producerInterface
import time
import threading
from typing import Any
import os

class mqProducer(producerInterface):
    def __init__(self, routing_key : str, pub_delay : int, message_producer : Any) -> None:
        self.m_routing_key = routing_key
        self.m_pub_delay = pub_delay
        self.m_pub_producer = message_producer
        self.m_run = threading.Event()
        self.m_pool = ThreadPoolExecutor(max_workers=1)
        self.setupRMQConnection()

    def __del__(self):
        print(f"Closing RMQ connection on destruction")
        self.m_connection.close()


    def setupRMQConnection(self):
        conParams = pika.URLParameters(os.environ['AMQP_URL'])
        
        #Using blocking connection isn't safe across threads. Only use this within a single thread.
        #Our current threadpool has a max of 1 work.
        self.m_connection = pika.BlockingConnection(parameters=conParams)
        self.m_channel = self.m_connection.channel()
        
        #Create the exchange if not already present
        self.m_exchange = 'RMQ Labs'
        self.m_channel.exchange_declare(self.m_exchange)
   
   #Build our connection to the RMQ Connection.
#The AMPQ_URL is a string which tells pika the package the URL of our AMPQ service in this scenario RabbitMQ.
conParams = pika.URLParameters(os.environ['AMQP_URL'])
connection = pika.BlockingConnection(parameters=conParams)
channel = connection.channel()
channel.exchange_declare('Test Exchange')

#We can then publish data to that exchange using the basic_publish method
channel.basic_publish('Test Exchange', 'Test_route', 'Hi',...)

# We'll first set up the connection and channel
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare the topic exchange
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# Set the routing key and publish a message with that topic exchange:
routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(
    exchange='topic_logs', routing_key=routing_key, body=message)
print(f" [x] Sent {routing_key}:{message}")