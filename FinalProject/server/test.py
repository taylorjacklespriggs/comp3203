from socket import *
from sock_rw import *
import struct
from sys import argv
import os

addr = '192.168.0.25'

assert len(argv) == 3, 'Please enter the port and filename as arguments'
audioFile = open(argv[2], 'rb')
port = int(argv[1])

s = socket(AF_INET, SOCK_STREAM)
s.connect((addr, 3711))

u = socket(AF_INET, SOCK_DGRAM)
u.bind(('', port))

try:
    items = {'title': argv[2]}

    write_dict(s, items)
    resp = read_string(s)
    print("server responded with %r"%resp)

    if resp == b'wait':
        write_int(s, port)
        data, addr = u.recvfrom(132)
        port, token = struct.unpack('>i128s', data)
        print("Port and Token: %d, %r"%(port, token))
        print("Token length: %d"%len(token))
        try:
            t = socket(AF_INET, SOCK_STREAM)
            t.connect((addr, port))
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
