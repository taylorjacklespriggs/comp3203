import socket
import threading
from constants import MAX_ACCEPT, MAX_SLEEP

class TCPServer:
    def __init__(self, name, port, on_conn, log):
        self.__port = int(port)
        self.__sock = socket.socket(\
            socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(\
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind(('', self.__port))
        self.__sock.settimeout(MAX_SLEEP)
        self.__on_conn = on_conn
        self.__thread = threading.Thread(target=self.__run)
        self.__check_fin = None
        self.__log = log
        self.__name = name
    def __run(self):
        self.__sock.listen(MAX_ACCEPT)
        self.__log(("%s server listening for "\
            + "%d new connections on TCP:%d")%\
                (self.__name, MAX_ACCEPT, self.__port))
        try:
            while self.__check_fin():
                try:
                    self.__on_conn(self.__sock.accept())
                    self.__log("%s server accepted a new client"\
                        %self.__name)
                except socket.timeout:
                    pass
        except Exception as e:
            self.__log("%s server closed unexpectedly: %s"\
                %(self.__name, e))
        finally:
            self.__sock.close()
    def start(self, stopfunc):
        self.__check_fin = stopfunc
        self.__thread.start()
    def stop(self):
        self.__sock.close()
        self.__thread.join()
    def get_port(self):
        return self.__port

