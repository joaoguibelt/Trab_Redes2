from client import Client
import socket
from threading import Thread
from pynput import keyboard

#THREAD
class ThreadWithReturnValue(Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


#CONEXAO INICIAL
def initialize(name, ip, port):
    s_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s_send.connect(("localhost", 5000))
    s_send.sendto('connection stablished'.encode(), ("localhost", 5000))
    s_send.sendto(name.encode(),  ("localhost", 5000))
    s_send.sendto(ip.encode(),  ("localhost", 5000))
    s_send.sendto(str(port).encode(),  ("localhost", 5000))
    s_send.close()

    s_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_receive.bind((ip, port))
    s_receive.listen()
    conn, address = s_receive.accept()

    data = conn.recv(1024).decode()
    print(data)
    s_receive.close()

#LIGACAO
def calling(host, end_point):
    try:
        client = Client(host[0],host[1])
        thread.start_new_thread(client.send_audio,(end_point[0],6000))
        server = Server()
        server.reproduzir(host[0],6000)
    except:
        print("Error: unable to start thread")


#ENVIO DE CONVITE
#Realizar consulta no banco
def consultar(nome):
    global ip
    global port

    s_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_send.connect(("localhost", 5000))

    s_send.sendto('search'.encode(), ("localhost", 5000))
    s_send.sendto(ip.encode(), ("localhost", 5000))
    s_send.sendto(str(port).encode(), ("localhost", 5000))
    s_send.sendto(nome.encode(), ("localhost", 5000))


    s_send.close()


    s_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_receive.bind((ip, port))
    s_receive.listen()
    conn, address = s_receive.accept()

    data = conn.recv(1024).decode()
    s_receive.close()
    aux_list = list(map(str, data.split("$")))

    aux_list[2] = int(aux_list[2])
    return aux_list

#Convidar
def convidar(nome, ip, port):
    aux_list = consultar(nome)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))
    s.sendto("convite".encode(),(aux_list[1],aux_list[2]))
    while True:
        data, end = s_cli.recvfrom(10000)
        if data is not None:
            if data.decode() == "rejeitado":
                print("Usuário destino ocupado!")
                s.close()
            elif data.decode() == "aceito":
                s.close()
                calling((ip,port),(aux_list[1],aux_list[2]))

#ESCUTAR TECLADO
def on_press(key):
    global port
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['c', 's']:  # keys of interest
        if k == 'c':
            print("Entrei aqui")
            nome_destino = input()
            convidar(nome_destino, socket.gethostbyname("localhost"), port)
        #elif s == 's':
            #MOSTRA O BANCO DE DADOS / TABELA
        return False  # stop listener; remove this if want more keys


name = input("Qual seu nome?") #dario
ip = socket.gethostbyname("localhost")
port = int(input()) #3333
print(ip)
initialize(name, ip, port)
print("Bobeira")
s_cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_cli.bind((ip, port+1)) #3334
listener = keyboard.Listener(on_press=on_press)
listener.start()
while True:
    print("Testando")
    data, end = s_cli.recvfrom(10000)
    twrv = ThreadWithReturnValue(input, "O que deseja fazer?")
    twrv.start()

    if data is not None:
        # RECEBIMENTO DE CONVITE
        if data.decode() == "convite":
            print("Você foi convidado!")
            res_invite = input("Deseja participar da ligação? aceito/rejeitado")
            s_cli.sendto("resposta_ao_convite".encode(), end)
            s_cli.sendto(res_invite.encode(),end)
            if res_invite == "aceito":
                calling((ip,port),end)
            else:
                print("Convite rejeitado com sucesso!")
    else:
        print("Bobeira")
