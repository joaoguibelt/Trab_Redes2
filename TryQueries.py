import sqlite3
banco = sqlite3.connect('dataregister.db')
cursor = banco.cursor()
name = "Joao"
ip = "127.0.0.1"
port = 6789
cursor.execute("SELECT * FROM registros")
print(cursor.fetchall())