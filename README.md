# Chat-Sample-App
This is sample/starter code for programming assignments in the Distributed Systems course taught by Prof. Fábio M. Costa at UFG (first semester, 2022).
The app has a very simple client-server architecture. The aim is to identify the limitations/problems/issues and make enhancements at three levels: architectural, non-functional aspects, functional aspects.  

Overall architecture of this first version of the app (discussed in classroom):

![Chat Design - client-server](https://user-images.githubusercontent.com/13460193/173588387-89793ac9-17b9-4441-986b-53cac6ee40f4.png)

Passos para execução:

1) Acessar repositório

$:> cd python

2) Executar o seguinte para gerar os protótipos

$:> python3 -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/chatserver.proto

3) Editar o arquivo "const.py" como no exemplo a seguir |CHAT_SERVER_HOST = "172.17.0.2:50051"|. Altere o endereço dos usuários também.

4) Executar Server gRPC

$:> python3 chatserver.py

5) Executar os clientes, um exemplo para seguir abaixo.

$:> python3 chatclient.py Alice
