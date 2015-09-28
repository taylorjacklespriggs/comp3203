from socket import *
from client import Client
from threading import Thread

class ServerThread(Client):
    def __init__(self, serv, sock):
        Client.__init__(self, sock)
        self._serv = serv
    def start(self):
        '''
        passes the servers connection handler
        a byte stream then removes this client
        '''
        self._serv.get_method()(self)
        self._serv.remove_client(self)
        self.close()

class Server:
    def __init__(self, port, method):
        self._method = method
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._sock.bind(('', port))
        self._clients = set()
    def get_method(self):
        return self._method
    def remove_client(self, clnt):
        self._clients.remove(clnt)
    def start(self):
        '''
        sets up the socket to listen for incomming
        connections, then starts a new thread and
        passes the new socket to the method from
        the constructor
        '''
        self._sock.listen(10)
        print("Server listening for new connections")
        try:
            while True:
                print("Server accepting a new connection")
                cl, addr = self._sock.accept()
                print("Incoming connection from %r on port %r"%addr)
                cl = ServerThread(self, cl)
                self._clients.add(cl)
                Thread(target=cl.start).start()
        except KeyboardInterrupt:
            print('Keyboard interrupt')
        finally:
            for cl in self._clients:
                cl.close()
            self._sock.close()

if __name__ == '__main__':
    def loop(cl):
        i, o = cl.get_buffers()
        while True:
            o.write_string("Hello world!")
            print(i.read_string())
    s = Server(int(open('port').read().strip('\n')), loop)
    s.start()

