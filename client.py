import socket
import os
import datetime
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
        if self.connected:
            s.sendall(b"/dir".encode())
            response = s.recv(4096).decode()
            if response == "SUCCESS":
                pass
            else:
                pass
        else:
            print("Not connected to any server.")

    # Fetches a file from the server using a file name
    def fetch_file(self, filename):
        if self.connected:
            s.sendall(b"/get {filename}".encode())
            response = s.recv(4096).decode()
            if response.startswith(b"FILE"):
                print("File received from Server: {filename}")
                with open(filename, 'wb') as file:
                    file.write(response)
            else:
                print("Error: File not found in the server.")
        else:
            print("Not connected to any server.")

    # Sends a file to the server using the current client alias
    def send_file(self, filename):
        if self.connected:
            if os.path.exists(filename):
                with open(filename, 'rb') as file:
                    fileData = file.read()
                    s.sendall(f"/store {filename}".encode())
                    s.sendall(fileData)
                    response = s.recv(1024).decode()
                    if response == "SUCCESS":
                        time = datetime.now()
                        print("{self.userName} {time}: Uploaded {filename}")
                    else:
                        print("Error: Unsuccessful in sending file")
            else:
                print("Error: File not found.")
        else:
            print("Not connected to any server.")

    # registers the User
    def register_alias(self, user):
        if self.connected:
            s.sendall(b"/register {user}".encode())
            response = s.recv(1024).decode()
            if response == "SUCCESS":
                self.userName = user
                print("Welcome {self.userName}!")
            else:
                print("Error: Registration failed. Handle or alias already exists.")
        else:
            print("Not connected to any server.")


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