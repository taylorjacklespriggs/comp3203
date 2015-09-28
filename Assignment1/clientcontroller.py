from socket import *
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
            #TODO: Make part of Client UI or throw exception
            print("Invalid parameters for put.")
            return

        src_file = args[0]
        print(src_file)

        send_file = open(src_file, "r", encoding="ascii")

        i, o = self.client.get_buffers()
        o.write_string("put")
        o.write_int(1)
        o.write_string(src_file.split('/')[-1])

        res = i.read_string()
        print(res)

        o.write_file(send_file)
        send_file.close()

    def get(self, args):
        print("GET test")
        pprint.pprint(args)
        if len(args) > 2 or len(args) < 1:
            #TODO: Make part of Client UI or throw exception
            print("Invalid parameters for get.")
            return

        srcfile = args[0]
        dstfile = args[1]
