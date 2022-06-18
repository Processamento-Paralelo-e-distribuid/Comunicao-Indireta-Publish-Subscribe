# Comunica o Indireta - (Publish-Subscribe)
## Objetivo
Experimentar a implementação de sistemas de comunicação indireta por meio de middleware Publish/Subscribe (Pub/Sub) com Filas de Mensagens.

- Sincronizar a troca de mensagens entre os componentes do sistema.

- Utilizar brokers para gerenciamento da fila de mensagens na implementação de sistemas distribuídos.

## Desenvolvimento
O código foi elaborado seguindo o mesmo esquema dos codigos anteriores com um servidor e um cliente, onde o cliente faz chamadas por meio do **Subscribe** requisitando o desafio atrelado ao ID da transição mais atual, também faz publicação da seed encontrada, por meio do **Publish** para que o servidor receba e analise se a seed passada é a que resolve o desafio.

## Analise Exploratoria
### Acerto de erros
O código anterios apreseentava um pequeno erro referente a verificação se a seed encontrada é valida, nele o comparador analisa o valor de challenger e com para se os zeros no inicio possue a mesma quantidade do valor do challenger, porém não é o correto pois deve ser feita a conversam de hexadecimal para binarios dos digitos e posteriormente verificar a quantidade de challenger.
Contudo o erro foi consertado, e os resultados podem ser devidamente observados logo abaixo.
### Execução do progama
O programa do cliente executa fazendo assinatura pelo challenger e pelos resultados, para poder gerar seeds do desafio proposto e para saber se o desafio já foi solucionado respctivamente, o cliente também faz publicações constantes no seed para publicar suas proprias seed encontradas localmente.

Já para o servido é feito o contrario, uma assinatura de subscribe para receber as possiveis seeds que resolvam o desafio e duas assinaturas de publish para publicar no challenger o desafio atrelado a transição atual e outra para publicar o resultado, referente ao cliente que solucionou o desafio. 

Como rabbit possue uma memoria, mesmo que o cliente demore um tempo para fazer a assinatura no canal do challenger, ele receberar da mesma forma o desafio referente ultima transação.


A vantagem deste sistema e que:
- o cliente não necessita de conhecer conhecer o servidor, apenas a comunicação com o broker e suficiente.
- o cliente e o servidor não necessitam de estar a funcionar ao mesmo tempo, não necessitando que o cliente espere que o servidor esteja funcionando para rodar.
Melhor desempenho
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
```
