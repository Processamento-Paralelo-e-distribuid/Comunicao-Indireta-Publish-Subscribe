import pika, sys, os

def main():
    
    def callback(ch, method, properties, body):     #challenge
        print("Received %r" % body.decode())
    
    def callback2(ch, method, properties, body):    #result
        print("Received %r" % body.decode())

    connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
    channel = connection.channel()

    channel.queue_declare(queue = 'ppd/seed')       #publica
    channel.queue_declare(queue = 'ppd/challenge')  #assina
    channel.queue_declare(queue = 'ppd/result')     #assina

    channel.basic_publish(exchange = '', routing_key = 'ppd/seed', body = 'seed')
    channel.basic_consume(queue = 'ppd/challenge' , on_message_callback = callback, auto_ack = True)
    #channel.basic_consume(queue = 'ppd/result' , on_message_callback = callback2, auto_ack = True)

    print('Waiting for messages. To exit press CRTL+C')

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)