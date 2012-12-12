#!/usr/bin/env python
import pika
import uuid
import sys
import pickle

#
# based on code from:
#    http://www.rabbitmq.com/tutorials/tutorial-six-python.html
#

class RevertRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='kanga-toast.ecs.soton.ac.uk'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, op):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='celery_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=op)
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)

if __name__ == "__main__":
    revert_rpc = RevertRpcClient()

    op = sys.argv[1]

    print " [x] Requesting remote Capture-HPC server start..."
    response = revert_rpc.call(op)
    print " [.] Got " + response
