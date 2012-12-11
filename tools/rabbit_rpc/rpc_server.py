#!/usr/bin/env python
import pika
import subprocess
import os
import pickle

#
# based on code from:
#    http://www.rabbitmq.com/tutorials/tutorial-six-python.html
#

revert_path = "/home/cso1g09/capture-server"
vixpass = "fred"
allowedvms = ["[mystere-localDisk2] kanga-cereal/kanga-cereal.vmx"]

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='kanga-toast.ecs.soton.ac.uk'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def revert(args):
    cmd = os.path.join(revert_path, "revert")
    #cmd = "echo"
    if len(args) < 8:
        return "Error: Bad Argument List"
    args[2] = vixpass
    if args[3] not in allowedvms:
        print args[3]
        return "Error: VM not in list of allowed VMs!"

    p = subprocess.Popen([cmd] + args, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

    ret = p.communicate()

    return str(ret[0]) + "\n" + str(ret[1])

def on_request(ch, method, props, body):
    args = pickle.loads(str(body))

    print " [.] reverting VM...",
    response = revert(args)
    print "done!"
    ch.basic_publish(exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id = \
        props.correlation_id),
        body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()
