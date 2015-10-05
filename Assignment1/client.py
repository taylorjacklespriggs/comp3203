from threading import Thread
from _thread import interrupt_main, exit
from bytebuffer import ByteBuffer
from os import kill, getpid
from signal import SIGINT
from socket import timeout, SHUT_WR

class Client:
    def __init__(self, sock, main_interrupt=False):
        self._inter_main = main_interrupt
        self._sock = sock
        self._sock.settimeout(1)
        self._in_buffer = ByteBuffer()
        self._out_buffer = ByteBuffer()
        self._read_thread = Thread(target=self._recv)
        self._write_thread = Thread(target=self._send)
        self._open = True
        self._read_thread.start()
        self._write_thread.start()
    def _recv(self):
        '''
        reads constantly into the buffer
        '''
        try:
            while self._open:
                try:
                    bts = self._sock.recv(4096)
                    if not len(bts):
                        raise OSError()
                    self._in_buffer.write_bytes(bts)
                except timeout:
                    pass
        except OSError:
            print("Socket closed")
            self.close()
    def _send(self):
        '''
        writes the out buffer to the socket
        '''
        try:
            while self._open:
                bts = self._out_buffer.flush()
                while len(bts):
                    sent = self._sock.send(bts)
                    bts = bts[sent:]
        except OSError:
            self._close()
    def get_buffers(self):
        return self._in_buffer, self._out_buffer
    def close(self):
        if self._open:
            self._open = False
            self._out_buffer.close()
            try:
                self._sock.shutdown(SHUT_WR)
                self._sock.close()
            except OSError:
                pass
            print("Closing input buffer")
            self._in_buffer.close()
            print("Closed input buffer")
            try:
                self._read_thread.join()
                self._write_thread.join()
            except RuntimeError:
                if self._inter_main:
                    print("Interrupting main thread")
                    kill(getpid(), SIGINT)

if __name__ == '__main__':
    from socket import *
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('127.0.0.1', int(open('port').read().strip('\n'))))
    c = Client(s)
    i, o = c.get_buffers()
    while True:
        print(i.read_string())
        o.write_string("Hey there!")

