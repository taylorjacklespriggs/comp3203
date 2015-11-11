from socket import *
from sock_rw import *
import struct
from sys import argv
import os

assert len(argv) > 1, 'Please enter the filename as an argument'
audioFile = open(argv[1], 'rb')

s = socket(AF_INET, SOCK_STREAM)
s.connect(('127.0.0.1', 3711))

u = socket(AF_INET, SOCK_DGRAM)
u.bind(('', 2000))

try:
    items = {'title': argv[1]}

    write_dict(s, items)
    resp = read_string(s)
    print("server responded with %r"%resp)

    if resp == b'wait':
        write_int(s, 2000)
        data, addr = u.recvfrom(132)
        port, token = struct.unpack('>i128s', data)
        print("Port and Token: %d, %r"%(port, token))
        print("Token length: %d"%len(token))
        try:
            t = socket(AF_INET, SOCK_STREAM)
            t.connect(('127.0.0.1', port))
            write_bytes(t, token)
            print("Sent token to server")
            result = read_string(t)
            print("Stream thread responded with %r"%result)
            if result == b'go':
                length = 1
                while length:
                    bts = audioFile.read(1024)
                    write_string(t, bts)
                    length = len(bts)
        finally:
            t.close()
except Exception as e:
    print(e)
finally:
    s.close()
    u.close()
    print("Closed sockets")
