from client import Client
import socket
#Estabelecer conexão com registro - logar

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 55554))
s.sendto('search'.encode(), ("localhost", 55554))
s.sendto('Dario'.encode(), ("localhost", 55554) )
data, end = s.recvfrom(10000)
data_aux = data.decode()
print(f"testando  \n{data_aux}")
s.sendto('show data'.encode(),  ("localhost", 55554))
data, end = s.recvfrom(10000)
data_aux = data.decode()
print(f"testando  \n{data_aux}")
"""
name = "Dario"
ip = "localhost"
port = 6767

cliente = Client(name, ip, port)

while True:
    #Estabelecer conexão com registro


    #PEGAR O DESTINO NO REGISTRO

    #ENVIO DE CONVITE PARA O DESTINO

    #ENVIO DE PACOTE DE ÁUDIO
    cliente.send_audio(end_name, end_ip, end_port)

    #ESCUTAR RESPOSTA DO DESTINO
"""