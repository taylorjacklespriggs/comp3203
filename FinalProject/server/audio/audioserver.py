from audio.sink.alsasink import AlsaSink
from socket import *
from threading import Event

class AudioServer:
    def __init__(self, sink, frame_size, source=None):
        self.__sink = sink
        self.__frame_size = frame_size
        self.__audio_stream = source
        self.__buffer = b''
        self.__done = Event()
    def set_source(self, source):
        self.__audio_stream = source
    def get_source(self):
        return self.__audio_stream
    def start(self):
        self.__done.clear()
        while not self.__done.is_set():
            bts = self.__audio_stream.read()
            self.__buffer += bts
            if len(self.__buffer) >= self.__frame_size:
                lo = len(self.__buffer) % self.__frame_size
                self.__sink.write_frames(self.__buffer[:len(self.__buffer)-lo])
                self.__buffer = self.__buffer[:-lo]
    def stop(self):
        self.__done.set()

if __name__=='__main__':
    from audio.sink.alsasink import AlsaSink
    asnk = AlsaSink()
    asnk.change_state(2, 2, 44100)
    asrv = AudioServer(open('./audio/output', 'rb'), asnk, 2)
    asrv.start()

