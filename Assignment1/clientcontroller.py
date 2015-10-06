from socket import *
import os
from client import *
import clientui

class ClientController:
    def __init__(self, ip_addr):
        self.server_addr = ip_addr
        self.client = None
        self._ui = None

    def start(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.server_addr, int(open('port').read().strip('\n'))))
        self.client = Client(s, True)
        i, _ = self.client.get_buffers()
        res = i.read_string()
        output = i.read_string()
        assert res == 'success', 'Server rejected connection: %s'%output

        self._ui = clientui.ClientUI(self, output)
        self._ui.start()
        self.client.close()

    def ls(self, args):
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
        if len(args) > 2 or len(args) < 1:
            self._ui.display_error("Invalid parameters for put.")
            return

        # Get local file name and open the file
        try:
            src_file = args[0]
            send_file = open(src_file, "rb")
        except OSError as err:
            self._ui.display_error(str(err))
            return

        # Send 'put' and number of arguments
        i, o = self.client.get_buffers()
        o.write_string("put")
        o.write_int(len(args))

        # Determine destination file name and send the file name
        dst_filename = src_file.split('/')[-1] if len(args) < 2 else args[1]
        o.write_string(dst_filename)

        # Wait for 'ready'
        res = i.read_string()
        if res == 'inval':
            err = i.read_string()
            self._ui.display(err)
            return

        # Send the file, close it
        o.write_file(send_file)
        send_file.close()

        # Wait for reply
        res = i.read_string()
        if res == 'failed':
            err = i.read_string()
            self._ui.display_error(str(err))


    def get(self, args):
        if len(args) > 2 or len(args) < 1:
            self._ui.display_error("Invalid parameters for get.")
            return

        src_file = args[0]

        # Open temp file
        filename = src_file.split('/')[-1]
        if len(args)==1 or args[1]=='.':
            dst_file = filename
        else:
            dst_file = args[1]

        # Send 'get' and number of arguments
        i, o = self.client.get_buffers()
        o.write_string("get")
        o.write_int(len(args))

        # Send source of file
        o.write_string(src_file)

        res = i.read_string()
        if res == 'failed':
            err = i.read_string()
            self._ui.display_error(str(err))
            return

        try:
            incoming_file = open('{p}.tmp'.format(p=dst_file), "wb+")
            o.write_string('ready')
        except OSError as err:
            self._ui.display_error(str(err))
            o.write_string('failed')
            return

        # Receive incoming file
        i.read_file(incoming_file)
        try:
            incoming_file.close()
            os.rename('{p}.tmp'.format(p=dst_file), dst_file)
        except OSError as err:
            self._ui_display_error(str(err))
