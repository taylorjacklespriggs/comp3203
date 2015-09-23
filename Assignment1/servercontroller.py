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

    def _abs_dir(self, path, clis):
        if not path.startswith('/'):
            path = '/'.join((clis.current_directory, path))
        return path

    def list_files(self, i, o, clis):
        ### get the path from  i
        path = i.read_string()
        if path[0] != '/':
            path = clis.current_directory + '/' + path
        try:
            output = ls(path)
            status = 'success'
        except:
            status = 'inval'
            output = 'The path %s is not valid'%path
        o.write_string(status)
        o.write_string(output)

    def change_dir(self, i, o, clis):
        ### change directory
        num = i.read_int()
        if num == 0:
            clis.reset_directory()
            result = 'success'
            output = clis.current_directory
        else:
            assert num == 1, 'Client sent too many arguments'
            path = i.read_string()
            try:
                clis.current_directory = \
                        cd(self._abs_dir(path, clis))
                result = 'success'
                output = clis.current_directory
            except:
                result = 'inval'
                output = 'The directory %s does not exist'%path
        o.write_string(result)
        o.write_string(output)

    def put_in_file(self, i, o, clis): pass

    def get_file(self, i, o, clis): pass

    def handle_client(self, cl):
        clis = clientsession.ClientSession(cd("."))
        print("client created")
        i, o = cl.get_buffers()
        o.write_string('success')
        o.write_string(clis.current_directory)
        while True:
            message = i.read_string()
            try:
                print(message)
                self._commands[message](i, o, clis)
            except Exception as e:
                print(e)
                print("Server received an invalid command")
                o.write_string("inval")
                o.write_string("There was an invalid command: %s"%message)

if __name__ == '__main__':
    import server
    s = ServerController()
    s.start()
