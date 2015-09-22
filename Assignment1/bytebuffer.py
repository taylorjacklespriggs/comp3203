import struct
from threading import Semaphore

class ByteBuffer:
    def __init__(self):
        self._vals = []
        self._read_index = 0
        self._counter = Semaphore(0)
        self._has_vals = Semaphore(0)
    def _add_to_buffer(self, bts):
        l = len(self._vals)
        self._vals.append(bts)
        self._counter.release()
        if l == 0:
            self._has_vals.release()
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
        if len(self._vals) == 0:
            self._has_vals.acquire()
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
    def write_bytes(self, bts):
        self._add_to_buffer(bts)
    def write_file(self, f):
        '''
        takes in an open file for writing
        '''
        f.seek(0, 2)
        flen = f.tell()
        self.write_string(str(flen))
        f.seek(0)
        while flen:
            r = f.read(1024)
            flen -= len(r)
            self.write_string(r)
    def read_char(self):
        return self._flush(1)
    def read_int(self):
        return struct.unpack(">I", self._flush(4))[0]
    def read_string(self):
        l = self.read_int()
        return self._flush(l)
    def read_bytes(self, num):
        return self._flush(num)
    def read_file(self, f):
        '''
        takes in an open file ready for writing
        '''
        sz = int(self.read_string())
        while sz:
            r = self.read_string()
            f.write(r)
            sz -= len(r)
    def flush(self):
        self._has_vals.acquire()
        self._counter.acquire()
        bts = b''.join(self._vals)
        self._vals = []
        self._read_index = 0
        self._counter.release()
        return bts
    def close(self):
        self._has_vals.release()

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

