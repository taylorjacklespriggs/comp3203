from socket import *
import os

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

    def put_in_file(self, i, o, clis):
        # Get arguments
        num = i.read_int()
        print(num)

        # Get destination file name and determine path
        filename = i.read_string()
        print(filename)

        path = '{d}/{f}'.format(d=clis.current_directory, f=filename)
        print(path)

        # Open temporary file
        try:
            incoming_file = open('{p}.tmp'.format(p=path), "wb+")
        except Exception as err:
            o.write_string('inval')
            o.write_string('REMOTE SERVER: {e}'.format(e=str(err)))
            return

        # Indicate readiness, receive file and close, rename file
        o.write_string('ready')
        i.read_file(incoming_file)
        incoming_file.close()
        os.rename('{p}.tmp'.format(p=path), path)

        o.write_string('success')


    def get_file(self, i, o, clis): 
        # Get arguments
        num = i.read_int()
        print(num)

        # Get source path/filename
        src_file = i.read_string()
        path = '{d}/{f}'.format(d=clis.current_directory, f=src_file)
        print(path)

        msg = i.read_string()
        if msg == 'ready':
            print(msg)
            send_file = open(src_file, "rb")
            o.write_file(send_file)
            send_file.close()
            o.write_string('success')

    def handle_client(self, cl):
        clis = clientsession.ClientSession(cd("."))
        print("client created")
        i, o = cl.get_buffers()
        o.write_string('success')
        o.write_string(clis.current_directory)
        try:
            while True:
                message = i.read_string()
                try:
                    print(message)
                    self._commands[message](i, o, clis)
                except KeyError as e:
                    print("Server received an invalid command")
                    o.write_string("inval")
                    o.write_string("There was an invalid command: %s"%message)
                except CallException as e:
                    print(e.args[0])
                    o.write_string("inval")
                    o.write_string(e.args[0])
        except Exception as e:
            print(e.args[0])

if __name__ == '__main__':
    import server
    s = ServerController()
    s.start()
