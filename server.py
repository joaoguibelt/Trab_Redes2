import socket
import pyaudio

class Server:

    def reproduzir(self, ip, port):
        print("Entrei no server")

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        CHUNK = 1024
        audio = pyaudio.PyAudio()
        output_stream = audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=1,frames_per_buffer=4096)
        #binding IP and port
        s.bind((ip, port))
        print(f"Server started in {ip} : {port}")
        print("Waiting for Client response...")
        #receiving data from client
        while True:
            data_rev, end = s.recvfrom(1024)
            output_stream.write(data_rev)
            print("Chamada em andamento...")
