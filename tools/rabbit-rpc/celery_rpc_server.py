#!/usr/bin/env python
import pika
import subprocess
import os
import pickle

#
# based on code from:
#    http://www.rabbitmq.com/tutorials/tutorial-six-python.html
#

capture_path = "/home/cso1g09/capture-server"

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='celery_queue')

def revert(op):
    if "start" in op:
        jar = path.join(capture_path, "CaptureServer.jar")
        cmd = ["java", "-jar", jar, "-s", "10.0.0.254:7070", "start"]
        #Popen
        fd, fname = tempfile.mkstemp(prefix="cap")

        p = Popen(cmd, stdout=fd)
    if "stop" in op:
        p.terminate()
        #unlink(fname)

    #cmd = "echo"

    return "Operation success!"

def on_request(ch, method, props, body):
    args = str(body)

    print " [.] starting Capture-HPC server...",
    response = revert(args)
    print "done!"
    ch.basic_publish(exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id = \
        props.correlation_id),
        body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='celery_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()
