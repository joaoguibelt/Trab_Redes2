import socket
import pyaudio


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
        addressAux = address
        if address is not None:
            print('received: ' + data + '\nfrom: ' + address[0] + '\nlistening on port: ' + str(address[1]))
            while True:

                if addressAux != address:
                    s.sendto('rejeitado', address)
                elif data == 'convite':
                    print('responda com aceito ou reijeitado')
                    resposta = input()
                    s.sendto(resposta, address)
                    data = 0
                elif data == 'encerrar_ligação':
                    break
                elif data == 'aceito':
                    audio = pyaudio.PyAudio()
                    output_stream = audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=1,
                                               frames_per_buffer=4096)
                    while True:
                        data, address = s.recvfrom(1024)
                        output_stream.write(data)
                        if data == 'encerrar_ligação':
                            break
                elif data == 'rejeitado':
                    break
