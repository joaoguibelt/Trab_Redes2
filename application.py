from client import Client
from server import Server
import socket
from threading import Thread
from pynput import keyboard
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
import pyaudio


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
    s_send.connect((ip_registro, 5000))
    s_send.sendto('c'.encode(), (ip_registro, 5000))
    s_send.sendto(f"{name}${ip}${port}".encode(),  (ip_registro, 5000))
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
    print("Chamada iniciada!")

    threads = []
    client = Client()
    server = Server()
    client_thread = Thread(target=client.send_audio, args=[end_point[0], 6000])
    server_thread = Thread(target=server.reproduzir, args=[host[0], 6000])
    client_thread.start()
    #server.reproduzir(host[0], 6000)
    threads.append(client_thread)
    threads.append(server_thread)
    for i in threads:
        i.join()





#ENVIO DE CONVITE
#Realizar consulta no banco
def consultar(nome):
    global ip_host
    global port

    s_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_send.connect((ip_registro, 5000))
    s_send.sendto('s'.encode(), (ip_registro, 5000))
    s_send.sendto(f"{nome}${ip_host}${port}".encode(), (ip_registro, 5000))


    s_send.close()


    s_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_receive.bind((ip_host, port))
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
    s_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_send.bind((ip, 7000))
    s_send.sendto(f"convite: {name_host}".encode(),(aux_list[1],8000))
    print(f"{nome} foi convidado com sucesso!")

    data, end = s_send.recvfrom(1024)
    if data is not None:
        if data.decode() == "rejeitado":
            print("Usu??rio destino ocupado!")
            s_send.close()
        elif data.decode() == "aceito":
            s_send.close()
            print("Chamando...")
            calling((ip,6000),(aux_list[1],6000))
        s_send.close()

#ESCUTAR TECLADO
def on_press(key):
    global port
    global  ip_host
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['c']:  # keys of interest
        if k == 'c':
            nome_destino = input("Digite o nome de quem deseja convidar:")
            convidar(nome_destino, ip_host, port)
        elif s == 's':
            table()
        return False  # stop listener

#MOSTRAR DADOS
def show_data():
    global ip_registro
    global ip_host
    global port

    s_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_send.connect((ip_registro, 5000))
    s_send.sendto('d'.encode(), (ip_registro, 5000))
    s_send.sendto(f"{nome}${ip_host}${port}".encode(), (ip_registro, 5000))
    s_send.close()


    s_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_receive.bind((ip_host, port))
    s_receive.listen()
    conn, address = s_receive.accept()
    data = conn.recv(1024).decode()
    s_receive.close()
    return data

def table():
    users = list(map(str, show_data().split("$")))
    count = 0
    for i in users:
        if count < 2:
            print(f"{i} | ", end="")
        else:
            print(f"{i}")
            count = 0
    print("")


#ACEITAR/REJEITAR INVITE
def listen_invite(ip):
    s_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_receive.bind((ip, 8000))
    data, end = s_receive.recvfrom(1024)

    if "convite" in data.decode():
        #MOSTRAR NA TELA A OP????O
        convite, nome = map(str, data.decode().split(": "))
        aux_list = consultar(nome)
        #Aceitar
        if accept_reject(nome):
            s_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s_send.sendto("aceito".encode(), (aux_list[1], 7000))
            s_send.close()
            print("Conectando...")
            calling((ip,6000), (aux_list[1],6000))
        #Rejeitar
        else:
            s_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s_send.sendto("rejeitado".encode(), (aux_list[1], 7000))
            s_send.close()

def accept_reject(nome):
    res = mb.askquestion('Convite',
                         f'{nome} te convidou para uma conversa, quer participar?')
    var = ""
    if res == 'yes':
        return True
    else:
        return False

ip_registro = "10.10.10.252" # IP DO SERVER DE REGISTRO
name_host = input("Qual seu nome?")
ip_host = input("Qual IP da sua m??quina?") #IP DA M??QUINA
port = int(input("Qual a porta para sua aplica????o escutar?")) #3333
print(ip_host)
initialize(name_host, ip_host, port)
s_cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_cli.bind((ip_host, port))
#table()
print("Aperte C para enviar convite :")
listener = keyboard.Listener(on_press=on_press)
listener.start()
lister_invite = Thread(target=listen_invite, args=[ip_host])
lister_invite.start()

"""while True:
    print("Testando")
    data, end = s_cli.recvfrom(10000)
    if data is not None:
        # RECEBIMENTO DE CONVITE
        if data.decode() == "convite":
            print("Voc?? foi convidado!")
            res_invite = input("Deseja participar da liga????o? aceito/rejeitado")
            s_cli.sendto("resposta_ao_convite".encode(), end)
            s_cli.sendto(res_invite.encode(), end)
            if res_invite == "aceito":
                calling((ip_host, port), end)
            else:
                print("Convite rejeitado com sucesso!")
    else:
        print("Bobeira")
"""