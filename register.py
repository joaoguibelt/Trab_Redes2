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
host = "192.168.1.3"
port = 5000
entry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
entry.bind((host, port))

while True:
    entry.listen()
    print("Aguardando conexão")
    conn, address = entry.accept()

    data = conn.recv(1).decode()

    #INITIALIZE
    if  "c" in data:
        data = conn.recv(1024).decode()
        aux_list = list(map(str, data.split("$")))
        print(aux_list)
        exit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        exit.connect((aux_list[1], int(aux_list[2])))
        register =  connect(aux_list[0], aux_list[1], aux_list[2])
        if register:

            exit.sendto("Usuário já cadastrado anteriormente".encode(), (aux_list[1],int(aux_list[2])))
            exit.close()
            entry.close()
            entry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            entry.bind((host, 5000))

        else:
            print("Cai no else")
            exit.sendto("Cadastro realizado".encode(), (aux_list[1],int(aux_list[2])))
            exit.close()
            entry.close()
            entry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            entry.bind((host, 5000))


    #CONSULTAR/CONVIDAR
    elif  "s" in data:

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


    elif data == "d":
        users = show_data()
        conn.sendto(users.encode(), address)
