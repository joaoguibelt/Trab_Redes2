from Cliente import *
import socket

def cli_ser():
    host = ''
    port = 6000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))

    while True:
        s.listen()
        print('waiting to receive message')
        data, address = s.recvfrom(1024)
        if address != None:
            print('received: ' + data + '\nfrom: ' + address[0] + '\nlistening on port: ' + str(address[1]))
            while True:
                if data == 'convite':
                    resposta = input()
                    s.sendto(resposta, address)
                elif data == 'encerrar_ligação':
                    # implementar
                    break
                elif data == 'resposta_ao_convite':
                    s.sendto(data, address)


cli_ser()
