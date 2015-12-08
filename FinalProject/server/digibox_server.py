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
    def __init__(self, dport, lport, sport, pport, paswd, max_queue = MAX_QUEUE):
        self.__disc_port = int(dport)
        self.__disc_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__disc_sock.bind(('', self.__disc_port))
        self.__disc_sock.settimeout(MAX_SLEEP)
        self.__disc_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__disc_thread = threading.Thread(target=self.__bcast_responder)
        self.__disc_msg = bytearray(DISCOVERY_PACKET_SIZE)
        self.__list_server = TCPServer(\
            "new connection", lport, self.__handle_client,\
            self.__log)
        self.__str_server = TCPServer(\
            "stream", sport, self.__handle_stream,\
            self.__log)
        self.__play_server = TCPServer(\
            "playback", pport, self.__handle_playback,\
            self.__log)
        struct.pack_into('>ii%ds'%len(DISCOVERY_HEADER),\
                self.__disc_msg, 0, self.__list_server.get_port(),\
                self.__play_server.get_port(), DISCOVERY_HEADER)
        self.__password = paswd
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
        self.__stream_lock = threading.Semaphore(1)
    def __check_password(self, pwd):
        return pwd == self.__password
    def __play_pause(self):
        if self.__pause.is_set():
            self.__pause.clear()
        else:
            self.__pause.set()
    def __next(self):
        self.__next_song.set()
    def __bcast_responder(self):
        print("Responding to broadcasts on port %d"%self.__disc_port)
        while self.__go():
            try:
                _, addr = self.__disc_sock.recvfrom(0)
                self.__disc_sock.sendto(self.__disc_msg, addr)
                print("Responded to broadcast at %s:%d"%addr)
            except socket.timeout:
                pass
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
            write_int(c_sock, self.__device_queue.qsize())
    def __accept_streams(self):
        while self.__go():
            try:
                self.__stream_lock.acquire()
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
                    self.__stream_lock.release()
            except queue.Empty:
                self.__stream_lock.release()
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
                        self.__next_stream = None
                        write_string(c_sock, b'go')
                        self.__audio_lock.acquire()
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
        threading.Thread(target=target).start()
    def __get_info(self):
        return dict()
    def __handle_playback(self, conn):
        sock, addr = conn
        actions = {\
                b'play': self.__play_pause,\
                b'pause': self.__play_pause,\
                b'next': self.__next\
                }
        def check_then_play(vals):
            if self.__check_password(vals[b'password']):
                try:
                    actions[vals[b'action']]()
                    write_string(sock, b'done')
                    return
                except:
                    pass
            write_string(sock, b'fail')
        def request_info(_):
            write_dict(sock, self.__get_info())
        actions = {\
                b'playback': check_then_play,\
                b'getinfo': request_info,\
                }
        def target():
            req = read_dict(sock, on_timeout=self.__gohard)
            self.__log("Client requested %r"%req)
            try:
                actions[req[b'request']](req)
            except Exception as e:
                self.__log("request %r failed: %s"%(req, e))
            sock.close()
        threading.Thread(target=target).start()
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
            self.__stream_lock.release()
            ffplay.communicate()
            print("ffplay finished")
    def __log(self, msg):
        self.__log_queue.put(msg)
    def __logger(self):
        while self.__go():
            try:
                print(self.__log_queue.get(True, MAX_SLEEP))
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
            self.__str_server.start(self.__go)
            self.__accept_thread.start()
            self.__list_server.start(self.__go)
            self.__play_server.start(self.__go)
            sleep(MAX_SLEEP)
            self.__disc_thread.start()
            while True:
                key = input()
                if key == 'n':
                    self.__next()
                elif key == 'p':
                    self.__play_pause()
        except KeyboardInterrupt:
            self.__is_done.set()
            self.__audio_lock.release()
            self.__stream_lock.release()
            self.__next()

if __name__ == '__main__':
    import os
    try:
        dport = os.getenv('DPORT', DISCOVERY_PORT)
        lport = os.getenv('LPORT', '3711')
        sport = os.getenv('SPORT', '3912')
        pport = os.getenv('PPORT', '4172')
        DigiboxServer(dport, lport, sport, pport, PASSWORD).start()
    except ValueError:
        print("Please enter integers for port numbers")

