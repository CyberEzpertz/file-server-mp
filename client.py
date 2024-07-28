import socket
s = socket.socket()

def parser(inp):
        return inp.split(' ')

class userConnection:
    def __init__(self):
        self.userName = None
        self.connected = False
        
        self.server_IP = None
        self.portNumber = None
        

    # Fetches a file from the server using a file name
    def fetch_dir(self):
        pass

    # Fetches a file from the server using a file name
    def fetch_file(filename):
        pass

    # Sends a file to the server using the current client alias
    def send_file(filename):
        pass

    # registers the User
    def register_alias(self, user):
        self.userName = user

    # Disconnects from the current server
    def server_disconnect(self):
        s.close()
        s = socket.socket()
        self.connected = False

    # Connects with the server
    def server_connect(self):
        s.connect((self.server_IP, self.portNumber))
        self.connected = True


    # Prints the commands and their functions
    def print_help():
        print("""
            Available commands:
            /join <server_ip_add> <port> - creates a connection with the server
            /leave - leaves the connection with the server
            /register <handle> - registers a user
            /store <filename> - send a file to the server
            /dir - requests a list of file names stored with the server
            /get <filename> - requests the specific file from the directory of the server
            /? - gets all input syntax commands shown above for reference
            """)


# Ask for input while client is open
while True:
    inp = input("> ")
    client = userConnection();
    wordList = parser(inp)
    commandWord = wordList[0]
    if commandWord == '/join':
        client.server_IP = wordList[1]
        client.port = int(wordList[2])
        client.server_connect()
    elif commandWord == '/leave':
        client.server_disconnect()
    elif commandWord == '/register':
        client.register_alias(wordList[1])
        client.userName = wordList[1]
    elif commandWord == '/store':
        fileName = wordList[1]
        client.send_file(fileName)
    elif commandWord == '/dir':
        client.fetch_dir()
    elif commandWord == '/get':
        fileName = wordList[1]
        client.fetch_file(fileName)
    elif commandWord == '/?':
        client.print_help()

    if wordList[0] == "/exit":
        print("See you on the flip side")
        break