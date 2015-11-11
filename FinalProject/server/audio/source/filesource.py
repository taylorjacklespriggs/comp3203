import os
from audio.source.audiostreamsource import AudioStreamSource
from subprocess import Popen, PIPE
from threading import Thread, Event
import tempfile
import socket
from time import sleep

class FileSource(AudioStreamSource):
    def __init__(self, source, channels=1, width=2, rate=44100, port=47243):
        self.__source = source
        self.get_num_frames = lambda: -1
        self.get_num_stored_bytes = lambda: 0
        self.get_num_channels = lambda: channels
        self.get_sample_width = lambda: width
        self.get_sample_rate = lambda: rate
        self.__frame_width = self.get_sample_width() * self.get_num_channels()
        self.__ffmpeg = Popen(['./audio/decoder', '-c', str(channels), \
                '-w', str(width), '-r', str(rate), '-p', str(port)], \
                env={"FFMPEG": "./audio/ffmpeg"}, \
                stdout=PIPE, bufsize=2**16)
        sleep(0.1)
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Client socket connecting on port %d"%port)
        self.__client_socket.connect(("127.0.0.1", port))
        self.__done = Event()
        def write_pipe(self):
            while True:
                bts = self.__source.read(1024)
                if not len(bts):
                    break
                print("Sending bts", len(bts))
                while len(bts):
                    bts = bts[self.__client_socket.send(bts):]
                    print("bts left", len(bts))
            print("Done writing")
            self.__client_socket.close()
        self.__write = Thread(target=lambda:write_pipe(self))
        self.__write.daemon = True
        self.__write.start()
        self.__leftover = b''
    def read_frames(self, num):
        num *= self.__frame_width
        print(num)
        print("Receiving bts")
        while len(self.__leftover) < num and not self.__done.is_set():
            self.__ffmpeg.stdout.flush()
            bts = self.__ffmpeg.stdout.read(num)
            if not len(bts):
                break
            self.__leftover += bts
        print("Len leftover", len(self.__leftover))
        if len(self.__leftover) < num:
            ret = self.__leftover
            self.__leftover = b''
            return ret
        ret, self.__leftover = self.__leftover[:num], self.__leftover[num:]
        print(len(ret))
        return ret

