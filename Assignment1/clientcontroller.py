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
        
        print(self.server_addr)
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.server_addr, int(open('port').read().strip('\n'))))
        self.client = Client(s)
        #i, o = client.get_buffers()
        #while True:
            #print(i.read_string())
            #o.write_string("Hey there!")

        self._ui = clientui.ClientUI(self)
        self._ui.start()
        self.client.close()

    def ls(self, args):
        print("LS test")
        pprint.pprint(args)
        if len(args) > 1:
            return "Invalid parameters for ls."

        i, o = self.client.get_buffers()
        o.write_string("ls");
        o.write_string(args[0] if len(args) else '.');
        res = i.read_string()
        if res == 'success':
            return i.read_string()
        raise Exception(i.read_string())


    def cd(self, args):
        print("CD test")
        pprint.pprint(args)
        if len(args) > 1:
            #TODO: mAke part of client UI
            print("Invalid parameters for cd.")
        return "NEW DIRECTORY"
    
    def put(self, args):
        print("PUT test")
        pprint.pprint(args)
        if len(args) > 2 or len(args) < 1:
            #TODO: Make part of Client UI or throw exception
            print("Invalid parameters for put.")
            return

    def get(self, args):
        print("GET test")
        pprint.pprint(args)
        if len(args) > 2 or len(args) < 1:
            #TODO: Make part of Client UI or throw exception
            print("Invalid parameters for get.")
            return

        srcfile = args[0]
        dstfile = args[1]
