from socket import *

import server
import clientsession
from calls import *

class ServerController:
    def __init__(self):
      self.server = self._open_server()
      self._commands = {'ls': self.list_files,
                        'cd': self.change_dir,
                        'put': self.put_in_file,
                        'get': self.get_file}

    def _open_server(self):
        return server.Server(int(open('port').read().strip('\n')), self.handle_client)

    def start(self):
        self.server.start()

    def list_files(self, i, o, clis):
        ### get the path from  i
        path = i.read_string()
        
        o.write_string(ls(clis.directory))

    def change_dir(self, i, o, clis): pass
        ### change directory

    def put_in_file(self, i, o, clis): pass

    def get_file(self, i, o, clis): pass

    def handle_client(self, cl):
        clis = clientsession.ClientSession(cd("."))
        print("client created")
        i, o = cl.get_buffers()
        while True:
            message = i.read_string()
            print(message)
            try:
                o.write_string("Test worked!")
                ### self._commands[message](i, o, clis)
            except:
                print("Server received an invalid command")
                o.write_string("inval")
                o.write_string("There was an invalid command: %s"%message)

if __name__ == '__main__':
    import server
    s = ServerController()
    s.start()
