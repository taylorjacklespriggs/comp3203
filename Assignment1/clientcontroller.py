from socket import *
import os
import pprint
from client import *
import clientui
#import clientsession

class ClientController:
    def __init__(self, ip_addr):
        #self.session = clientsession.ClientSession("./gibberish")
        self.server_addr = ip_addr
        self.client = None
        self._ui = None

    def start(self):
        #print(self.session)

        #print(self.server_addr)
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.server_addr, int(open('port').read().strip('\n'))))
        self.client = Client(s)
        i, _ = self.client.get_buffers()
        res = i.read_string()
        output = i.read_string()
        assert res == 'success', 'Server rejected connection: %s'%output

        self._ui = clientui.ClientUI(self, output)
        self._ui.start()
        self.client.close()

    def ls(self, args):
        #pprint.pprint(args)
        assert len(args) <= 1, \
            "Invalid parameters for ls."

        i, o = self.client.get_buffers()
        o.write_string("ls");
        o.write_string(args[0] if len(args) else '.');
        res = i.read_string()
        output = i.read_string()
        assert res == 'success', 'Server could not process command: %s'%output
        self._ui.display(output)

    def cd(self, args):
        #pprint.pprint(args)
        assert len(args) <= 1, \
            "Invalid parameters for cd."

        i, o = self.client.get_buffers()
        o.write_string("cd")
        o.write_int(len(args))
        for a in args:
            o.write_string(a)
        res = i.read_string()
        output = i.read_string()
        assert res == 'success', 'Server could not change directory: %s'%output
        self._ui.change_dir(output)

    def put(self, args):
        print("PUT test")
        pprint.pprint(args)
        if len(args) > 2 or len(args) < 1:
            self._ui.display_error("Invalid parameters for put.")
            return

        # Get local file name and open the file
        src_file = args[0]
        print(src_file)
        send_file = open(src_file, "rb")

        # Send 'put' and number of arguments
        i, o = self.client.get_buffers()
        o.write_string("put")
        o.write_int(len(args))

        # Determine destination file name and send the file name
        dst_filename = src_file.split('/')[-1] if len(args) < 2 else args[1]
        o.write_string(dst_filename)

        # Wait for 'ready'
        res = i.read_string()
        print(res)

        # Send the file, close it
        o.write_file(send_file)
        send_file.close()

        # Wait for reply
        res = i.read_string()
        print(res)

    def get(self, args):
        print("GET test")
        pprint.pprint(args)
        if len(args) > 2 or len(args) < 1:
            #TODO: Make part of Client UI or throw exception
            print("Invalid parameters for get.")
            return

        # Send 'get' and number of arguments
        i, o = self.client.get_buffers()
        o.write_string("get")
        o.write_int(len(args))

        # Send source of file
        src_file = args[0]
        print(src_file)
        o.write_string(src_file)

        # Open temp file
        filename = src_file.split('/')[-1]
        if len(args)==1 or args[1]=='.':
            dst_file = filename
        else:
            dst_file = args[1]
        print(dst_file)
        incoming_file = open('{p}.tmp'.format(p=dst_file), "wb+")
        o.write_string('ready')
        print('Printint in {d}'.format(d=dst_file))

        # Receive incoming file
        i.read_file(incoming_file)
        incoming_file.close()
        os.rename('{p}.tmp'.format(p=dst_file), dst_file)

