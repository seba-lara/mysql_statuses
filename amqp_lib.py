import pika,sys,os
import datetime
import time
import json

class QueueConnection:
    pass

    def connection_to_exchange(host,port,usuario,password,exchange_name,queue_name):
        try:
            tiempo = datetime.datetime.now()
            credentials = None
            connection = None
            credentials = pika.PlainCredentials(usuario,password)
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=host,
                port=port,
                credentials=credentials
                )
            )
            channel = connection.channel()
                
            channel.exchange_declare(exchange='status', exchange_type='fanout',durable=True)

            result = channel.queue_declare(queue='catdog',exclusive=True)
            queue_name = result.method.queue
            channel.queue_bind(exchange='status', queue=queue_name)
            print('[*] Waiting for logs. To exit press CTRL+C')
            

            def callback(ch, method, properties, body):
                asd = (f" {tiempo} [x] %r" % body) # its a tuple
                print(" [x] Done")
                print(asd)

            channel.basic_consume(
                queue=queue_name, on_message_callback=callback, auto_ack=True)

            channel.start_consuming()
            
        except KeyboardInterrupt:
            print('Interrupted')
            channel.close()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)