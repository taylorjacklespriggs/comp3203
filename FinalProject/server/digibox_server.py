import socket
import threading
import queue
import os
import struct
from time import sleep
from sock_rw import *
import subprocess
from service_server import TCPServer

from constants import *

MAX_QUEUE = 17

TOKEN_LENGTH = 128

NOTIFY_ATTEMPTS = 5
NOTIFY_PAUSE = 1

def int_sleep(stime, on_tmo):
    while stime > 0 and on_tmo():
        tm = min(stime, MAX_SLEEP)
        sleep(tm)
        stime -= tm

class DigiboxServer:
    class FinishedException(Exception):
        pass
    class __QueuedDevice:
        def __init__(self, ip_addr, m_data):
            self.ip_addr = ip_addr
            self.m_data = m_data
            self.port = None
            self.sem = threading.Semaphore(0)
        def ready(self):
            self.sem.acquire()
        def set_port(self, port):
            self.port = port
            self.sem.release()
    class __QueuedStream:
        def __init__(self, token):
            self.token = token
            self.ev = threading.Event()
        def check_token(self, token):
            ret = self.token == token
            if ret:
                self.ev.set()
            return ret
        def checked(self):
            return self.ev.is_set()
    def __init__(self, dport, lport, sport, max_queue = MAX_QUEUE):
        self.__disc_port = int(dport)
        self.__disc_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__disc_sock.bind(('', self.__disc_port))
        self.__disc_sock.settimeout(MAX_SLEEP)
        self.__list_server = TCPServer(\
            "new connection", lport, self.__handle_client,\
            self.__log)
        self.__str_server = TCPServer(\
            "stream", sport, self.__handle_stream,\
            self.__log)
        self.__is_done = threading.Event()
        self.__next_song = threading.Event()
        self.__pause = threading.Event()
        self.__device_queue = queue.Queue(max_queue)
        self.__stream_queue = queue.Queue()
        self.__next_stream = None
        self.__log_queue = queue.Queue()
        self.__log_thread = threading.Thread(target=self.__logger)
        self.__accept_thread = threading.Thread(\
            target=self.__accept_streams)
        self.__audio_lock = threading.Semaphore(1)
    def __handle_client(self, conn):
        c_sock, c_addr = conn
        self.__log("Received a new client connection from %s:%d"%c_addr)
        def target():
            try:
                m_data = read_dict(c_sock, on_timeout=self.__gohard)
                self.__log("Received metadata from %r: %r"%(c_addr, m_data))
                self.__queue_device(conn, m_data)
            finally:
                c_sock.close()
        t = threading.Thread(target=target)
        t.start()
    def __queue_device(self, conn, m_data):
        c_sock, c_addr = conn
        try:
            device = DigiboxServer.__QueuedDevice(c_addr[0], m_data)
            self.__device_queue.put_nowait(device)
            self.__log("Queued device at %s"%c_addr[0])
            write_string(c_sock, b'wait')
            port = read_int(c_sock, self.__gohard)
            device.set_port(port)
            self.__log("Device at %s is waiting on UDP %d"%(c_addr[0], port))
        except queue.Full:
            self.__log("Queue is full, sorry %r"%c_addr[0])
            write_string(c_sock, b'full')
            write_int(c_sock, len(self.__device_queue))
    def __accept_streams(self):
        while self.__go():
            try:
                qd = self.__device_queue.get(True, MAX_SLEEP)
                qd.ready()
                token = self.__gen_token()
                stream = DigiboxServer.__QueuedStream(token)
                self.__stream_queue.put(stream)
                udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                tries = 0
                msg = struct.pack('>i', self.__str_server.get_port())\
                    + token
                while self.__go() and not stream.checked()\
                        and tries < NOTIFY_ATTEMPTS:
                    udp_sock.sendto(msg, (qd.ip_addr, qd.port))
                    int_sleep(NOTIFY_PAUSE, self.__go)
                    tries += 1
                    self.__log("Finished attempt %d to contact %s:UDP%d"%\
                            (tries, qd.ip_addr, qd.port))
                if not stream.checked():
                    self.__log(("Failed to contact %s for streaming, "\
                        + "moving on")%qd.ip_addr)
            except queue.Empty:
                pass
    def __handle_stream(self, conn):
        c_sock, c_addr = conn
        c_sock.settimeout(MAX_SLEEP)
        self.__log("Handling stream connection from %s:%d"%c_addr)
        def target():
            try:
                token = read_bytes(c_sock, TOKEN_LENGTH, self.__gohard)
                try:
                    while self.__go() and self.__next_stream is None:
                        try:
                            self.__next_stream = \
                                    self.__stream_queue.get(\
                                        True, MAX_SLEEP)
                        except queue.Empty:
                            pass
                    if self.__next_stream.check_token(token):
                        write_string(c_sock, b'go')
                        self.__audio_lock.acquire()
                        self.__next_stream = None
                        try:
                            if self.__go():
                                self.__playback(c_sock)
                        finally:
                            self.__audio_lock.release()
                    else:
                        write_string(c_sock, b'fail')
                except Exception as e:
                    self.__log(("There was a problem streaming "
                        + "from %s: %s")%\
                            (c_addr[0], e))
                finally:
                    self.__next_stream = None
            except Exception as e:
                self.__log("There was a problem with the stream: %s"%e)
            finally:
                c_sock.close()
        t = threading.Thread(target=target)
        t.start()
    def __playback(self, sock):
        ffplay = subprocess.Popen(['ffplay', '-i', '-', '-nodisp', '-autoexit'], \
                stdin=subprocess.PIPE, stderr=open(os.devnull, 'wb'))
        try:
            length = 1
            while length:
                if self.__next_song.is_set():
                    length = 0
                    self.__next_song.clear()
                elif self.__pause.is_set():
                    sleep(MAX_SLEEP)
                else:
                    bts = read_string(sock, self.__gohard)
                    ffplay.stdin.write(bts)
                    length = len(bts)
        finally:
            ffplay.stdin.write(b'')
            ffplay.stdin.close()
            print("Closed ffplay STDIN")
            ffplay.communicate()
            print("ffplay finished")
    def __log(self, msg):
        self.__log_queue.put(msg)
    def __logger(self):
        while self.__go():
            try:
                print(self.__log_queue.get(True, 0.1))
            except queue.Empty:
                pass
    def __gen_token(self):
        return os.urandom(TOKEN_LENGTH)
    def __go(self):
        return not self.__is_done.is_set()
    def __gohard(self):
        if self.__is_done.is_set():
            raise DigiboxServer.FinishedException()
        return True
    def start(self):
        try:
            self.__log_thread.start()
            self.__list_server.start(self.__go)
            self.__accept_thread.start()
            self.__str_server.start(self.__go)
            while True:
                key = input()
                if key == 'n':
                    self.__next_song.set()
                elif key == 'p':
                    if self.__pause.is_set():
                        self.__pause.clear()
                    else:
                        self.__pause.set()
        except KeyboardInterrupt:
            self.__is_done.set()

if __name__ == '__main__':
    import os
    try:
        dport = os.getenv('DPORT', '3513')
        lport = os.getenv('LPORT', '3711')
        sport = os.getenv('SPORT', '3912')
        DigiboxServer(dport, lport, sport).start()
    except ValueError:
        print("Please enter integers for port numbers")

