import ui
import clientui
import clientsession

class Controller:
    def __init__(self):
        '''do something here'''
    def start(self):
        print("Stuff")
        view = ui.UI()
        selection = view.start()
        print(selection)
        if selection == "server":
            print("Server will now start...")
        else:
            print("Connecting to server at {ip}...".format(ip=selection))
            session = clientsession.ClientSession("./gibberish")
            print(session)
            client_view = clientui.ClientUI(self)
            client_view.start()
    def ls(directory):
        print("ls command received: {1}".format(directory))
    def cd(directory):
        print("cd command received: {1}".format(directory))
    def put(srcfile, dstfile):
        print("put command received: {1}, {2}".format(srcfile, dstfile))
