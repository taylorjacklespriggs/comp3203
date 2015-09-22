from threading import Thread
from bytebuffer import ByteBuffer

class Client:
    def __init__(self, sock):
        self._sock = sock
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
        while self._open:
            self._in_buffer.write_bytes(self._sock.recv(4096))
    def _send(self):
        '''
        writes the out buffer to the socket
        '''
        while self._open:
            self._sock.send(self._out_buffer.flush())
    def get_buffers(self):
        return self._in_buffer, self._out_buffer
    def close(self):
        self._open = False
        self._sock.close()
        self._in_buffer.close()
        self._out_buffer.close()

if __name__ == '__main__':
    from socket import *
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('127.0.0.1', int(open('port').read().strip('\n'))))
    c = Client(s)
    i, o = c.get_buffers()
    while True:
        print(i.read_string())
        o.write_string("Hey there!")

