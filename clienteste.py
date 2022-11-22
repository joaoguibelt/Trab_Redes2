import socket
import pyaudio

ip = "192.168.1.3"
port = 6000

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
audio = pyaudio.PyAudio()
CHUNK = 1024
input_stream = audio.open(format=pyaudio.paInt16, input=True, rate=44100, channels=1, frames_per_buffer=CHUNK)
while True:

    data = input_stream.read(CHUNK, exception_on_overflow=False)
    s.sendto(data,(ip,port))
