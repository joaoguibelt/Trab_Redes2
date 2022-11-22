import socket
import pyaudio
import socket, pyaudio

class Client:

    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.CHUNK = 1024


    def send_audio(self, ip, port):
        audio = pyaudio.PyAudio()

        input_stream = audio.open(format=pyaudio.paInt16, input=True, rate=44100, channels=1, frames_per_buffer=self.CHUNK)
        output_stream = audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=1,frames_per_buffer=4096)
        while True:
               data = input_stream.read(self.CHUNK, exception_on_overflow=False)
               # print('cliente1')
               self.s.sendto(data,(ip,port))
               data_rev, end = self.s.recvfrom(10000)
               output_stream.write(data_rev)