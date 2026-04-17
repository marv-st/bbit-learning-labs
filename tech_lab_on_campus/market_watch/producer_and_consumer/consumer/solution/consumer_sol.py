import pika
import os

class mqConsumer(mqConsumerInterface):

    def __init__(self, binding_key: str, exchange_name: str, queue_name: str):
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.setupRMQConnection()
        
    def setupRMQConnection(self) -> None:
    # Set-up Connection to RabbitMQ service
    
    conParams = pika.URLParameters(os.environ['AMQP_URL'])
    self.m_connection = pika.BlockingConnection(parameters=conParams)
    
    # Establish Channel
    self.m_channel = self.m_connection.channel()
    
    # Create the exchange if not already present
    self.m_channel.exchange_declare(self.exchange_name)
    
    # Create Queue if not already present
    self.m_channel.queue_declare(queue=self.queue_name)
    
    # Bind Binding Key to Queue on the exchange
    self.m_channel.queue_bind(queue=self.queue_name, routing_key=self.binding_key, exchange=self.exchange_name)
    
    # Set-up Callback function for receiving messages
    self.m_channel.basic_consume(self.queue_name, self.on_message_callback)
    
    def on_message_callback(
        self, channel, method_frame, header_frame, body
    ) -> None:
        # Acknowledge message
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

        # Print message
        print(f" [x] Received {body.decode()}")
