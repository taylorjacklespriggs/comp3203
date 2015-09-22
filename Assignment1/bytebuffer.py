import struct
from threading import Semaphore

class ByteBuffer:
    def __init__(self):
        self._vals = []
        self._read_index = 0
        self._counter = Semaphore(0)
    def _add_to_buffer(self, bts):
        self._vals.append(bts)
        self._counter.release()
    def _flush(self, num):
        vals = []
        while num > 0:
            self._counter.aquire()
            l = len(self._vals[0])
            dl = l - self._read_index
            if dl < num: # pop the value from the queue
                val = self._vals.pop(0)
                vals.append(vals[self._read_index:])
                self._read_index = 0
                num -= dl
            else: # increment the read index and put the semaphore back
                end = self._read_index + num
                vals.append(self._vals[0][self._read_index:end])
                self._read_index = end
    def write_char(self, char):
        assert len(char) == 1, 'Not for writing strings'
        self._add_to_buffer(char)
    def write_int(self, val):
        self._add_to_buffer(struct.pack(">I", val))
    def write_string(self, string):
        self.write_int(len(string))
        self._add_to_buffer(string.encode('ascii'))
    def read_char(self):
        return chr(self._flush(1))
    def read_int(self):
        return struct.unpack(">I", self._flush(4))
    def read_string(self):
        l = self.read_int()
        return self._flush(l).decode('utf-8')

