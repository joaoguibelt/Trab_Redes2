import socket
import wave

import pyaudio
socket_Cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

porta_servidor = 12345
ip_servidor = '127.0.0.1'
porta_receber = 4096
descricao = ['nome', '127.0.0.2', porta_receber]
#variaveis para o audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def consulta(nome_Destino):
    socket_Cli.sendto(nome_Destino.encode("utf-8"),(ip_servidor,porta_servidor))
    ip_consulta,addr = socket_Cli.recvfrom(porta_receber)
    return(ip_consulta)

def convite():
    socket_Cli.sendto(descricao, (ip_servidor,porta_servidor))
    resposta_convite,addr = socket_Cli.recvfrom(porta_receber)
    if resposta_convite == 'negado':
        print("Usuário destino ocupado")
    elif resposta_convite == 'aceito':
        p = pyaudio.PyAudio()
        stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
        frames = []
        sair = 0

        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            wf = wave.open('audio.wav', 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            socket_Cli.sendto(wf, (ip_servidor, porta_servidor))
            ouvindo, addr = socket_Cli.recvfrom(porta_receber)
            if sair == 1:
                socket_Cli.sendto('encerrar_ligação', (ip_servidor, porta_servidor))
                break
            if ouvindo == 'encerrar_ligação':
                break
            else:
                wf2 = wave.open(ouvindo, 'rb')
                data = wf2.readframes(CHUNK)
                while len(data) > 0:
                    stream.write(data)
                    data = wf2.readframes(CHUNK)
                wf2.close()

        stream.stop_stream()
        stream.close()
        p.terminate()
