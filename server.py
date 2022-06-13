from multiprocessing.connection import Client
import pika, sys, os
import pandas as pd
import random

def getTransactionID(df):
    if(df is None):
        lista = {"TransactionID":[0], "Challenge":[random.randint(1,5)], "Seed":[" "], "Winner": [-1]}
        df = pd.DataFrame(lista)
    else:
        tam = len(df.iloc[:, 0])
        if(df.iloc[tam-1, 3]):
            return df.iloc[tam-1, 0]
        else:
            transactionID = df.iloc[(tam-1), 0]+1
            lista = {"TransactionID":[0], "Challenge":[random.randint(1,5)], "Seed":[" "], "Winner": [-1]}
            transaction = pd.DataFrame(lista)

            df = pd.concat([df,transaction], ignore_index = True)
    
    return transactionID

def getChallenge(transactionID, df):
    transaction = df.query("TransactionID ==" + str(transactionID))

    if(transaction.empty==False):
        return transaction["Challenge"].values[0]
    else:
        return -1

def callback(ch, method, proprerties, body):        #seed
    print("Received %r" % body.decode())
    lista = body.decode().split('/')

    clientID = lista[0]
    transactionID = lista[1]
    seed = lista[2]
    
    #channel.basic_publish(exchange = '', routing_key = 'ppd/result', body = 'result')

def main():

    lista = {"TransactionID":[0], "Challenge":[random.randint(1,5)], "Seed":[" "], "Winner": [-1]}
    df = pd.DataFrame(lista)

    print(df)
    
    transaction = getTransactionID(df)
    challenge = getChallenge(transaction, df)
    cod_challenge = str(transaction) + '/' + str(challenge)

    print(cod_challenge)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue = 'ppd/seed')       #assina
    channel.queue_declare(queue = 'ppd/challenge')  #publica
    channel.queue_declare(queue = 'ppd/result')     #publica

    channel.basic_consume(queue = 'ppd/seed', on_message_callback = callback, auto_ack = True)
    channel.basic_publish(exchange = '', routing_key = 'ppd/challenge', body = cod_challenge)

    channel.start_consuming()

    connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)