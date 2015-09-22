from UIException import *

class ClientUI:
    def __init__(self, controller):
        self.commands = {"h": self.showhelp, "ls": self.ls, "cd": self.cd,
                "put": self.put, "get": self.get}
        self.controller = controller

    def start(self):
        ''' starts the UI. Should be the main entry point '''
        while (1):
            print("Command(type h for list of commands): ")
            command = input().split(" ")
            result = self.parsecommand(command)
            if result == 1:
                break

    def parsecommand(self, command):
        ''' redirects the interface to call the correct function based on
            user input
            Returns 1 when the user wants to close the client connection'''
        try:
            if command[0] == "q":
                return 1;

            self.commands[command[0]](command[1:])
        except IndexError:
            print("Please enter a command")
        except KeyError:
            print("Please enter a valid command")

    def showhelp(self, args):
        ''' displays command help to the user for using the client '''
        print("Commands:\n\th - displays the command help\n\t" +
                "q -  stops the client\n\t" +
                "ls <directory> - lists everything in <directory>\n\t" +
                "cd <directory> - changes the current directory to <directory>\n\t" +
                "put <src> <dest> - put the src file from the client to the dest file on the server\n\t" +
                "get <src> <dest> - get the src file from the server to the destination file on the client\n\t")

    def ls(self, args):
        ''' asks the controller to return a list of everything in
            the current directory on the server'''
        try:
            if len(args):
                directorylist = self.controller.ls(args)
            else:
                directorylist = self.controller.ls(".")
            print(directorylist)
        except DirectoryError:
            print("Directory does not exist on the server...")

    def cd(self, args):
        ''' asks the controller to move the user to another directory on the
            server '''
        try:
            currentdirectory = self.controller.cd(args[0])
            print("Current directory: " + currentdirectory)
        except DirectoryError:
            print("Directory does not exist on the server...")

    def put(self, args):
        ''' sends the source filename and destination filename to the
            controller for transferring a file from the client to the server '''
        try:
            self.controller.put(args)
            print("transfer successful!")
        except PutServerError:
            print("Could not write to server...")
        except PutClientError:
            print("Could not find file on client...")

    def get(self, args):
        ''' sends the source filename and destination filename to the controller
            for transferring a file from the server to the client '''
        try:
            self.controller.get(args)
            print("transfer successful!")
        except GetServerError:
            print("Could not find file on server...")
        except GetClientError:
            print("Could not write file to client...")

if __name__ == "__main__":
    client = ClientUI()
    client.start()
