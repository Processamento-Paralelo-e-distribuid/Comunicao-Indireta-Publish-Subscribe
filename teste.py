from multiprocessing.connection import Client
import pika, sys, os
import pandas as pd
import random
from hashlib import sha1

global arquivo 
arquivo = 'banco-de-dados.csv'
def getTransactionID():
    try:
        df = pd.read_csv(arquivo)
        print("Arquivo encontrado")
    except:
        print("Criando Banco de dados")
        df = None
    transactionID = 0
        
    if(df is None):
        lista = {"TransactionID":[0], "Challenge":[random.randint(1,5)], "Seed":[" "], "Winner": [-1]}
        df = pd.DataFrame(lista)
    else:
        tam = len(df.iloc[:, 0])
        if(df.iloc[tam-1, 3]):
            return int(df.iloc[tam-1, 0])
        else:
            transactionID = df.iloc[(tam-1), 0]+1
            lista = {"TransactionID":[transactionID], "Challenge":[random.randint(1,5)], "Seed":[" "], "Winner": [-1]}
            transaction = pd.DataFrame(lista)
            
            df = pd.concat([df,transaction], ignore_index = True)
    
    df.to_csv(arquivo, index=False)
    
    return int(transactionID)

def getChallenge(transactionID):
    try:
        df = pd.read_csv(arquivo)
    except:
        return -1
    transaction = df.query("TransactionID ==" + str(transactionID))

    if(transaction.empty==False):
        return transaction["Challenge"].values[0]
    else:
        return -1

def submitChallenge(transactionID, ClientID, seed):
    try:
        df = pd.read_csv(arquivo)
    except:
        return -1
    
    trasition = df.query("TransactionID == "+str(transactionID))    
    
    if(trasition.empty == True):
        return -1
    elif(trasition["Winner"].values != -1):
        return 2
    
    texto = str(seed).encode('utf-8')
    hash = sha1(texto).hexdigest()
    
    challenge = trasition["Challenge"].values[0]
    
    
    if(True):
        trasition.loc[transactionID,"Seed"]   = str(seed)
        trasition.loc[transactionID,"Winner"] = ClientID
        df.iloc[transactionID,:] = trasition.iloc[0,:]
        
        df.to_csv(arquivo, index=False)
        return 1
    else:
        return 0
def main():

    def callback(ch, method, proprerties, body):        #seed
        print("Received %r" % body.decode())
        lista = body.decode().split('/')

        clientID = int(lista[0])
        transactionID = int(lista[1])
        seed = str(lista[2])
        print(clientID, transactionID, seed)
        
        cod_result = str(transactionID) + '/' + str(clientID) + '/' + seed
        
        resposta = submitChallenge(transactionID, clientID, seed)
        
        transactionID = getTransactionID()
        print(transactionID)
        while True:
            challenge = getChallenge(transactionID)
            if(challenge != -1):
                break
            else:
                transactionID = getTransactionID()
        
        cod_challenge = str(transactionID) + '/' + str(challenge)
        channel.basic_publish(exchange = '', routing_key = 'ppd/result', body = cod_result)
        channel.basic_publish(exchange = '', routing_key = 'ppd/challenge', body = cod_challenge)
    transactionID = getTransactionID()
    while True:
        challenge = getChallenge(transactionID)
        if(challenge != -1):
            break
        else:
            transactionID = getTransactionID()
    
    cod_challenge = str(transactionID) + '/' + str(challenge)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue = 'ppd/seed')       #assina
    channel.queue_declare(queue = 'ppd/challenge')  #publica
    channel.queue_declare(queue = 'ppd/result')     #publica

    channel.basic_publish(exchange = '', routing_key = 'ppd/challenge', body = cod_challenge)
    channel.basic_consume(queue = 'ppd/seed', on_message_callback = callback, auto_ack = True)

    channel.start_consuming()

    connection.close()

if __name__ == '_main_':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)