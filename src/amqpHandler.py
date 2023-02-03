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
        channel.queue_declare(queue=queue_name,exclusive=False,durable=False,auto_delete=True)
        channel.queue_bind(exchange=exchange_name, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for statuses. To exit press CTRL+C')
        channel.start_consuming()


"""def main():

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