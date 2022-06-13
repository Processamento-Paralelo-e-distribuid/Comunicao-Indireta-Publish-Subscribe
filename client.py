import pika, sys, os
import threading
import random
import string
from hashlib import sha1

def main():
    
    def callback(ch, method, properties, body):     #challenge
        print("Received %r" % body.decode())
        lista = body.decode().split('/')

        seed = []
        # 1 - TransactionID atual
        transactionID = lista[0]

        # 2 - Challenge(desafio) associada ao transactionID atual;
        challenger = lista[1]

        transactionID = int(transactionID)

        challenger = int(challenger)
        # 3 - Buscar, localmente, uma seed (semente) que solucione o desafio proposto
        flag = True

        text = "| ID da transação atual: "+str(transactionID)+", desafio associado: "+str(challenger)
        print(text)
        
        text = "| Procurando seed ..."
        print(text)
        
        def random_generator(size=6, n=1, chars=string.printable): # Gera string aleatória
            random.seed(n)
            return ''.join(random.choice(chars) for _ in range(size))
        def getSeed(challenger, seed, size): # Gera seed
            n = 0
            while(flag):
                seedTemp = random_generator(size, n)
                texto = str(seedTemp).encode('utf-8')
                hash = sha1(texto).hexdigest()
                
                if(hash[0:challenger] == "0"*challenger and hash[challenger] != "0"):
                    seed.append(seedTemp)
                    break
                n = n + 1

        multThread = []

        for i in range(1,challenger*2+1):
            thread = threading.Thread(target=getSeed, args=(challenger, seed, i, ))
            multThread.append(thread)
            thread.start()
            
            if(len(seed) > 0):
                flag = False
                break   

        while(True):
            if(len(seed) != 0):
                break

        flag = False

        # Verifica se todas as threads acabaram 
        for thread in multThread:
            thread.join()

        # 4 - Imprimir localmente a seed encontrada
        text = "| A seed encontrada é "+str(seed)
        print(text)
        
        # 5 - Submete seed ao servidor e espera resposta.
        ClientID = int(input("| Digite o ID do cliente: "))
        
        #enviar resposta para server
        cod_seed = str(ClientID)+'/'+str(transactionID)+'/'+str(seed)
        channel.basic_publish(exchange = '', routing_key = 'ppd/seed', body = cod_seed)
        
        # 6 - Imprime e decodfica resposta do servidor.
        """ text = ""
        if(resposta == -1):
            text = "| ID da transação invalido"
        elif(resposta == 0):
            text = "| A seed passada é invalida, logo não resolve o desafio"
        elif(resposta == 1):
            text = "| A seed passada é valida"
        elif(resposta == 2):
            text = "| O desafio já foi solucionado"
        print(text)
     """
    
    def callback2(ch, method, properties, body):    #result
        print("Received %r" % body.decode())
        lista = body.decode().split('/')

        # 1 - TransactionID atual
        transactionID = lista[0]

        # 2 - ClientID associada ao transactionID atual;
        clientID = lista[1]

        # 3 - Seed associada ao transactionID atual;
        seed = lista[2]

    connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
    channel = connection.channel()

    channel.queue_declare(queue = 'ppd/seed')       #publica
    channel.queue_declare(queue = 'ppd/challenge')  #assina
    channel.queue_declare(queue = 'ppd/result')     #assina

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