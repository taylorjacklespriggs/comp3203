import ui
import clientcontroller
import servercontroller

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
            servercontrl = servercontroller.ServerController()
            servercontrl.start()
        else:
            print("Connecting to server at {ip}...".format(ip=selection))
            clientcontrl = clientcontroller.ClientController(selection)
            clientcontrl.start()
