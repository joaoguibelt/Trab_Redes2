import sqlite3
import socket



def connect(name, ip, port):
    banco = sqlite3.connect('dataregister.db')
    cursor = banco.cursor()
    print("Entrou no connect")
    print(name)
    print(ip)
    print(port)
    cursor.execute("SELECT nome, ip, porta FROM registros "
                   f"WHERE nome = '{name}' AND ip = '{ip}'")
    aux = cursor.fetchall()
    print(aux)
    print("Saiu do connect")
    if aux == []:
        cursor.execute(f"INSERT INTO registros VALUES ('{name}','{ip}','{port}')")
        banco.commit()
        #Cadastro realizado
        return False
    else:
        #Usuário já cadastrado
        return True

def search(name):
    print("Name as "+ name)
    banco = sqlite3.connect('dataregister.db')
    cursor = banco.cursor()
    cursor.execute("SELECT nome, ip, porta FROM registros "
                   f"WHERE nome = '{name}'")
    aux_list = cursor.fetchall()
    print("Teste")
    print(aux_list)
    print(f"{aux_list[0][0]}${aux_list[0][1]}${aux_list[0][2]}")
    return f"{aux_list[0][0]}${aux_list[0][1]}${aux_list[0][2]}"

def show_data_aux():
    cursor.execute("SELECT nome FROM Registros")
    aux_list = cursor.fetchall()
    return aux_list

def show_data():
    aux_list = show_data_aux()
    users = ""
    for tuples in aux_list:
        print(tuples[0])
        users += tuples[0]
    return users

# MAIN
host = "localhost"
port = 5000
entry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
entry.bind((host, port))

while True:
    entry.listen()
    print("Aguardando conexão")
    conn, address = entry.accept()

    data = conn.recv(1024).decode()

    #INITIALIZE
    if data == "connection stablished":
        name = conn.recv(1024).decode() #name
        ip = conn.recv(1024).decode() #ip
        port = conn.recv(1024).decode() #port
        exit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        exit.connect((ip, int(port)))
        register =  connect(name, ip, port)
        if register:

            print(address)
            print(address[1])
            exit.sendto("Usuário já cadastrado anteriormente".encode(), (address[0],int(port)))
            exit.close()
            entry.close()
            entry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            entry.bind((host, 5000))

        else:
            print(address)
            print(address[1])
            exit.sendto("Cadastro realizado".encode(), (address[0],int(port)))
            exit.close()
            entry.close()
            entry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            entry.bind((host, 5000))


    #CONSULTAR/CONVIDAR
    elif data == "search":

        ip = conn.recv(1024).decode()  # ip
        port = conn.recv(1024).decode()  # port
        name = conn.recv(1024).decode() #name
        exit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        exit.connect((ip, int(port)))
        infos = search(name)
        print("INFOS? " + infos)
        exit.sendto(infos.encode(), address)
        exit.close()
        entry.close()
        entry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        entry.bind((host, 5000))


    elif data == "show data":
        users = show_data()
        conn.sendto(users.encode(), address)
