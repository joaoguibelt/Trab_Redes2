import socket
import pyaudio


ip = "192.168.1.3"
port = 6000
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
       data, end = s.recvfrom(10000)
       output_stream.write(data)
       print("Chamada em andamento...")
       # output_stream.write(data)
s.close()
