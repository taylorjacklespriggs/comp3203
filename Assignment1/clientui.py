from UIException import *
import sys

class ClientUI:
    def __init__(self, controller, current_dir, prompt='$ '):
        self.commands = {"h": self.showhelp, "ls": self.ls, "cd": self.cd,
                "put": self.put, "get": self.get}
        self.controller = controller
        self._dir = current_dir
        self._prompt = prompt

    def display(self, msg):
        sys.stdout.write(msg)
        sys.stdout.write('\n')

    def display_error(self, msg):
        sys.stderr.write(msg)
        sys.stderr.write('\n')

    def get_input(self):
        vals, buff = [], []
        done = False
        prmpt = self._dir + self._prompt
        while not done:
            done = True
            inp = input(prmpt)
            i, j, l = 0, 0, len(inp)
            while i < l:
                if inp[i] == '\\':
                    if i + 1 < l: # add next char for sure
                        buff.append(inp[i + 1])
                        i += 1
                    else: # otherwise this is the end of the line
                        done = False
                elif inp[i] == ' ': # clear the char buffer
                    if len(buff):
                        vals.append(''.join(buff))
                        buff = []
                    j = i + 1
                else: # add the current char
                    buff.append(inp[i])
                i += 1
            prmpt = self._prompt
        if len(buff): # join the last chars
            vals.append(''.join(buff))
        return vals

    def start(self):
        ''' starts the UI. Should be the main entry point '''
        while (1):
            self.display("Command(type h for list of commands): ")
            command = self.get_input()
            result = self.parsecommand(command)
            if result == 1:
                break

    def change_dir(self, new_dir):
        self._dir = new_dir

    def parsecommand(self, command):
        ''' redirects the interface to call the correct function based on
            user input
            Returns 1 when the user wants to close the client connection'''
        try:
            if command[0] == "q":
                return 1;
            self.commands[command[0]](command[1:])
        except IndexError:
            self.display_error("Please enter a command")
        except KeyError:
            self.display_error("Please enter a valid command")
        except Exception as e:
            self.display_error(e.args[0])

    def showhelp(self, args):
        ''' displays command help to the user for using the client '''
        print(\
'''Commands:
    h - displays the command help
    q - stops the client
    ls <directory> - lists everything in <directory>
    cd <directory> - changes the current directory to <directory>
    put <src> <dest> - put the src file from the client to the
                        destination file on the server
    get <src> <dest> - get the src file from the server to the
                        destination file on the client''')

    def ls(self, args):
        ''' asks the controller to return a list of everything in
            the current directory on the server'''
        self.controller.ls(args)

    def cd(self, args):
        ''' asks the controller to move the user to another directory on the
            server '''
        self.controller.cd(args)

    def put(self, args):
        ''' sends the source filename and destination filename to the
            controller for transferring a file from the client to the server '''
        self.controller.put(args)

    def get(self, args):
        ''' sends the source filename and destination filename to the controller
            for transferring a file from the server to the client '''
        self.controller.get(args)

if __name__ == "__main__":
    client = ClientUI(None, '/')
    while True:
        print(client.get_input())

