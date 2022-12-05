#!/usr/bin/env python3
import pika

class QueueConnection:
    pass

    def connection_to_exchange(host,port,usuario,password):

        credentials = None
        connection = None
        credentials = pika.PlainCredentials(usuario,password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=credentials
            )
        )
        return connection

    def create_channel(connection,callback,exchange_name,queue_name):

        channel = connection.channel()
        channel.queue_declare(queue=queue_name,exclusive=False,durable=False)
        channel.queue_bind(exchange=exchange_name, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for statuses. To exit press CTRL+C')
        channel.start_consuming()


"""import pika,sys,os
import datetime
import time
import json

def main():
    tiempo = datetime.datetime.now()
    credentials = pika.PlainCredentials('tisa','tisa')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.75.10.166',port=5672,credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='status', exchange_type='fanout',durable=True)

    result = channel.queue_declare(queue='catdog',exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='status', queue=queue_name)
    print('[*] Waiting for logs. To exit press CTRL+C')
    
    def callback(ch, method, properties, body):
        asd = (f" {tiempo} [x] %r" % ) # its a tuple
        print(" [x] Done")
        print(asd)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)"""        