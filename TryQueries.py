import sqlite3
banco = sqlite3.connect('dataregister.db')
cursor = banco.cursor()
name = "Joao"
ip = "127.0.0.1"
port = 6789
cursor.execute("SELECT nome, ip, porta FROM registros "
                   f"WHERE nome = '{name}' AND ip = '{ip}'")

print(cursor.fetchall())
print("Mostrar tudo:")
name = "Dario"
cursor.execute("SELECT nome, ip, porta FROM registros "
                   f"WHERE nome = '{name}'")
print(cursor.fetchall())