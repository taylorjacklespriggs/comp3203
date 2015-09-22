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
            self._counter.acquire()
            l = len(self._vals[0])
            dl = l - self._read_index
            if dl <= num: # pop the value from the queue
                val = self._vals.pop(0)
                vals.append(val[self._read_index:])
                self._read_index = 0
                num -= dl
            else: # increment the read index and increment the sem
                end = self._read_index + num
                vals.append(self._vals[0][self._read_index:end])
                self._read_index = end
                self._counter.release()
                num = 0
        return b''.join(vals)
    def write_char(self, char):
        try:    char = char.encode('ascii')
        except: pass
        assert len(char) == 1, 'Not for writing strings'
        self._add_to_buffer(char)
    def write_int(self, val):
        self._add_to_buffer(struct.pack(">I", val))
    def write_string(self, string):
        string = string.encode('ascii')
        self.write_int(len(string))
        self._add_to_buffer(string)
    def read_char(self):
        return self._flush(1)
    def read_int(self):
        return struct.unpack(">I", self._flush(4))[0]
    def read_string(self):
        l = self.read_int()
        print(l)
        return str(self._flush(l), 'utf-8')

if __name__ == '__main__':
    bb = ByteBuffer()
    print("Writing int(3)")
    bb.write_int(3)
    print("Writing str('Hello world')")
    bb.write_string("Hello world")
    print("Writing chr('h')")
    bb.write_char('h')
    print("Reading integer: %d"%bb.read_int())
    print("Reading string: %s"%bb.read_string())
    print("Reading character: %s"%bb.read_char())

