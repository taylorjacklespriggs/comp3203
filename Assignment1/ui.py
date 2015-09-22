class UI:
    def __init__(self):
        '''do something here'''
    def start(self):
        print("Would you like to start a server? (y, n)")
        beServer = input()
        if beServer[0] == "y":
            print("Server has been started")
        else:
            print("Enter the ip address of the server you would like to connect to:")
            ip = input()

if __name__ == "__main__":
    ui = UI()
    ui.start()
