from Cliente import *


def cli_ser():
    host = ''
    port = 6000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))

    while True:
        print('waiting to receive message')
        data, address = s.recvfrom(1024)
        print('received: ' + data + '\nfrom: ' + address[0] + '\nlistening on port: ' + str(address[1]))

        if data == 'convite':
            resposta = input()
            s.sendto(resposta, address)
        elif data == 'encerrar_ligação':
            break
        elif data == 'respsota_ao_convite':
            data = input()
            s.sendto(data, address)


cli_ser()
