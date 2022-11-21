import sqlite3
import socket
banco = sqlite3.connect('dataregister.db')
cursor = banco.cursor()

def connect(name, ip, port):
    cursor.execute("SELECT nome, ip, porta FROM registros "
                   f"WHERE nome = {name} AND ip = {ip} AND porta = {port}")
    if cursor.fetchall() == []:
        cursor.execute(f"INSERT INTO registros VALUES ({name},{ip},{port})")
        #Cadastro realizado
        return False
    else:
        #Usuário já cadastrado
        return True

def search(name):
    cursor.execute("SELECT nome, ip, porta FROM registros "
                   f"WHERE nome = '{name}'")
    aux_list = cursor.fetchall()

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
port = 55554
entry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
entry.bind((host, port))

while True:
    entry.listen()
    print("Aguardando conexão")
    conn, address = entry.accept()
    while True:
        data = conn.recv(1024).decode()
        if data == "connection stablished":
            name = conn.recv(1024).decode() #name
            ip = conn.recv(1024).decode() #ip
            port = conn.recv(1024).decode() #port
            connect(name, ip, port)

        elif data == "search":
            name = conn.recv(1024).decode()  # name
            infos = search(name)
            conn.sendto(infos.encode(), address)

        elif data == "show data":
            users = show_data()
            conn.sendto(users.encode(), address)
        #
        # if connect(data):
        #     conn.sendto("Usuário já cadastrado anteriormente!", address)
        # else:
        #     conn.sendto("Usuário cadastrado com sucesso!", address)
