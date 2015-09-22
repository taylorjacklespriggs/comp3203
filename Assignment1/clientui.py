class ClientUI:
    def __init__(self):
        '''do something here'''

    def start(self):
        ''' starts the UI. Should be the main entry point '''
        while (1):
            print("Command(type h for list of commands): ")
            command = input()
            result = self.redirect(command)
            if result == 1:
                break

    def redirect(self, command):
        ''' redirects the interface to call the correct function based on
            user input
            Returns 1 when the user wants to close the client connection'''
        if command == "h":
            self.showhelp()
        if command == "q":
            return 1;

    def showhelp(self):
        ''' displays command help to the user for using the client '''
        print("Commands:\n\th - displays the command help\n\t" +
                "q -  stops the client\n\t")

if __name__ == "__main__":
    client = ClientUI()
    client.start()
