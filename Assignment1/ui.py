class UI:
    def __init__(self):
        '''do something here'''
    def start(self):
        print("Would you like to start a server? (y, n)")
        beServer = input()
        if beServer[0] == "y":
            print("Server attempting to start...")
            return "server"
        else:
            print("Enter the ip address of the server you would like to connect to:")
            ip = input()
            return ip

if __name__ == "__main__":
    ui = UI()
    ui.start()
