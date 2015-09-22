
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
        if command[0] == "q":
            return 1;

    def showhelp(self):
        ''' displays command help to the user for using the client '''
        print("Commands:\n\th - displays the command help\n\t" +
                "q -  stops the client\n\t" +
                "ls <directory> - lists everything in <directory>\n\t")

    def ls(self, directory):
        ''' asks the controller to return a list of everything in
            the current directory on the server'''
        directorylist = self.controller.ls(directory)
        print(directorylist)

    def cd(self, directory):
        ''' asks the controller to move the user to another directory on the
            server '''
        currentdirectory = self.controller.cd(directory)
        print("Current directory: " + currentdirectory)

if __name__ == "__main__":
    client = ClientUI()
    client.start()
