from socket import *
from sock_rw import *
import struct
from sys import argv
import os
from constants import DISCOVERY_PORT, DISCOVERY_PACKET_SIZE
import struct

assert len(argv) == 3, 'Please enter the port and filename as arguments'
filename = argv[2]
audioFile = open(filename, 'rb')
wait_port = int(argv[1])

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.sendto(b'', ('<broadcast>', DISCOVERY_PORT))
msg, addr = s.recvfrom(DISCOVERY_PACKET_SIZE)
list_port = struct.unpack('>i', msg[:4])[0]
ipaddr = addr[0]
print(list_port)

s = socket(AF_INET, SOCK_STREAM)
s.connect((ipaddr, list_port))

u = socket(AF_INET, SOCK_DGRAM)
u.bind(('', wait_port))

try:
    items = {'title': filename}

    write_dict(s, items)
    resp = read_string(s)
    print("server responded with %r"%resp)

    if resp == b'wait':
        write_int(s, wait_port)
        data, addr = u.recvfrom(132)
        str_port, token = struct.unpack('>i128s', data)
        print("Port and Token: %d, %r"%(str_port, token))
        print("Token length: %d"%len(token))
        try:
            t = socket(AF_INET, SOCK_STREAM)
            t.connect((ipaddr, str_port))
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
