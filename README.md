# Comunica o Indireta - (Publish-Subscribe)
## Objetivo
Experimentar a implementação de sistemas de comunicação indireta por meio de middleware Publish/Subscribe (Pub/Sub) com Filas de Mensagens.

- Sincronizar a troca de mensagens entre os componentes do sistema.

- Utilizar brokers para gerenciamento da fila de mensagens na implementação de sistemas distribuídos.

## Desenvolvimento
O código foi elaborado seguindo o mesmo esquema dos codigos anteriores com um servidor e um cliente, onde o cliente faz chamadas por meio do **Subscribe** requisitando o desafio atrelado ao ID da transição mais atual, também faz publicação da seed encontrada, por meio do **Publish** para que o servidor receba e analise se a seed passada é a que resolve o desafio.

## Analise Exploratoria

## Execução do progama

### **Local**
 [1] - Acesse a pasta onde estão localisados os arquivos do servidor e do cliente
 [2] - Execute o servidor utilizando o comando logo abaixo:
```
pyrhon3 serve.py
```
 [3] - Execute o cliente atravez do comando abaixo:
```
python3 cliente.py
```
### **Remoto** 
Altere em ambos os arquivos o localhost para o IP ao qual sera conectado o Broker
 [1] - Acesse a pasta onde estão localizados os arquivos do servidor e do cliente
 [2] - Execute o servidor utilizando o comando logo abaixo:
```
pyrhon3 serve.py
```
 [3] - Execute o cliente atravez do comando abaixo:
```
python3 cliente.py
``
