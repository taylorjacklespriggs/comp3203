from socket import *
from audio.audioserver import AudioServer
from audio.sink.alsasink import AlsaSink
import os
import signal
from asyncproc import Process
from threading import Thread
from time import sleep

channels = 1
sample_width = 2
sample_rate = 44100

audio_sink = AlsaSink()
audio_sink.change_state(channels, sample_width, sample_rate)
playback = AudioServer(audio_sink, channels * sample_width)

def force(f, *args):
    f(*args)

try:
    port = int(os.environ['PORT'])
except:
    port = 47231

server_socket = socket(AF_INET, SOCK_STREAM)
try:
    server_socket.bind(('', port))
finally:
    force(playback.stop)
server_socket.listen(1)
print("Server listening on port %d"%port)

try:
    while True:
        client, addr = server_socket.accept()
        try:
            print("Accepted connection from %s:%d"%addr)
            decode_process = Process(("./audio/decoder -c %d -r %d -w %d"%(\
                    channels, sample_rate, sample_width)).split(),\
                    env={"AUDIO_PATH":"./audio"})
            print("Started decoder")
            decode_pipe = decode_process
            print("Opened decode pipe")
            playback.set_source(decode_process)
            play_thread = Thread(target=playback.start)
            play_thread.start()
            print("Started playback thread")
            while True:
                bts = client.recv(1024)
                print(len(bts))
                if len(bts) < 1024:
                    decode_pipe.write(bts)
                    break
                while len(bts):
                    bts = bts[decode_pipe.write(bts):]
            decode_pipe.close()
            play_thread.join()
        except SocketException as e:
            print(e.strerror)
        client.close()
        decode_process.kill(signal.SIGTERM)
except KeyboardInterrupt:
    print("Stopping")
except Exception as e:
    print(e.strerror)
server_socket.close()
print("Closed server socket")

