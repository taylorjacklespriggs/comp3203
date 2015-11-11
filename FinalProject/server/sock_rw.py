import struct
import select
from socket import timeout

def read_bytes(sock, num, on_timeout=None):
    bts = b''
    while num and (on_timeout is None or on_timeout()):
        try:
            tmp = sock.recv(num)
            lt = len(tmp)
            if not lt:
                raise EOFError()
            assert lt <= num
            num -= lt
            bts += tmp
        except timeout:
            if on_timeout is None:
                raise e
    return bts

def read_int(sock, *args, **kwargs):
    return struct.unpack('>i', read_bytes(sock, 4, *args, **kwargs))[0]

def read_long(sock, *args, **kwargs):
    return struct.unpack('>q', read_bytes(sock, 8, *args, **kwargs))[0]

def read_string(sock, *args, **kwargs):
    return read_bytes(sock, read_int(sock, *args, **kwargs), *args, **kwargs)

def read_dict(sock, dest=dict(), *args, **kwargs):
    for _ in range(read_int(sock, *args, **kwargs)):
        key = read_string(sock, *args, **kwargs)
        value = read_string(sock, *args, **kwargs)
        dest[key] = value
    return dest

def write_bytes(sock, bts):
    while len(bts):
        bts = bts[sock.send(bts):]

def write_int(sock, i):
    write_bytes(sock, struct.pack('>i', i))

def write_long(sock, i):
    write_bytes(sock, struct.pack('>q', i))

def write_string(sock, st):
    try:
        st = st.encode('utf-8')
    except:
        pass
    write_int(sock, len(st))
    write_bytes(sock, st)

def write_dict(sock, dct):
    write_int(sock, len(dct))
    for k, v in dct.items():
        write_string(sock, k)
        write_string(sock, v)

