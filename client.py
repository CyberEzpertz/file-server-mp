import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    def fetch_file(self, filename):
        pass

    # Sends a file to the server using the current client alias
    def send_file(self, filename):
        pass

    # registers the User
    def register_alias(self, user):
        self.userName = user


    # Disconnects from the current server
    def server_disconnect(self):
        try:
            s.close()
            s = socket.socket()
            self.connected = False
            print("Connection closed. Thank you!")
        except socket.error as e:
            print("Error: Disconnection failed. Please connect to the server first.")


    # Connects with the server
    def server_connect(self):
        try:
            s.connect((self.server_IP, self.portNumber))
            self.connected = True
            print("Connection to the File Exchange Server is successful!")
        except socket.error as e:
            print("Error: Connection to the Server has failed! Please check IP Address and Port Number. ")


    # Prints the commands and their functions
    def print_help(self):
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

try:
    client = userConnection()
    while True:
        inp = input("> ")
        print(inp)
        wordList = parser(inp)
        cmd = wordList[0]

        match cmd:
            case '/join':
                client.server_IP = wordList[1]
                client.portNumber = int(wordList[2])
                client.server_connect()
            case '/leave':
                client.server_disconnect()
            case '/register':
                client.register_alias(wordList[1])
            case '/store':
                client.send_file(wordList[1])
            case '/dir':
                client.fetch_dir()
            case '/get':
                client.fetch_file(wordList[1])
            case '/?':
                client.print_help()
            case '/exit':
                print("See you on the flip side")
                s.close()
                break

except KeyboardInterrupt:
    print("Closing client, exiting.")
finally:
    # Close all connections to the server and the server itself
    s.close()