
class ClientUI:
    def __init__(self, controller):
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
        if command[0] == "h":
            self.showhelp()
        if command[0] == "ls":
            self.ls(command[1])
        if command[0] == "cd":
            self.cd(command[1])
        if command[0] == "put":
            self.put(command[1], command[2])
        if command[0] == "get":
            self.put(command[1], command[2])
        if command[0] == "q":
            return 1;

    def showhelp(self):
        ''' displays command help to the user for using the client '''
        print("Commands:\n\th - displays the command help\n\t" +
                "q -  stops the client\n\t" +
                "ls <directory> - lists everything in <directory>\n\t" +
                "cd <directory> - changes the current directory to <directory>\n\t" +
                "put <src> <dest> - put the src file from the client to the dest file on the server\n\t" +
                "get <src> <dest> - get the src file from the server to the destination file on the client\n\t")

    def ls(self, directory):
        ''' asks the controller to return a list of everything in
            the current directory on the server'''
        try:
            directorylist = self.controller.ls(directory)
            print(directorylist)
        except DirectoryError:
            print("Directory does not exist on the server...")

    def cd(self, directory):
        ''' asks the controller to move the user to another directory on the
            server '''
        try:
            currentdirectory = self.controller.cd(directory)
            print("Current directory: " + currentdirectory)
        except DirectoryError:
            print("Directory does not exist on the server...")

    def put(self, srcfile, destfile):
        ''' sends the source filename and destination filename to the
            controller for transferring a file from the client to the server '''
        try:
            self.controller.put(srcfile, destfile)
            print("transfer successful!")
        except PutServerError:
            print("Could not write to server...")
        except PutClientError:
            print("Could not find file on client...")

    def get(self, srcfile, destfile):
        ''' sends the source filename and destination filename to the controller
            for transferring a file from the server to the client '''
        try:
            self.controller.get(srcfile, destfile)
            print("transfer successful!")
        except GetServerError:
            print("Could not find file on server...")
        except GetClientError:
            print("Could not write file to client...")

if __name__ == "__main__":
    client = ClientUI()
    client.start()
