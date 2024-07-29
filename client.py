import socket
import os
from datetime import datetime

class userConnection:
    def __init__(self):
        self.userName = None
        self.connected = False
        self.server_IP = None
        self.portNumber = None
        self.sock = None


    def check_error(self, connection=True, name=False):
        error = None
        if connection and not self.connected:
            error = "Error: Not currently connected to a server."
        elif len(self.sock.recv(1024)) == 0:
            error = "Error: Server Connection has been severed. Try reconnecting or opening the server again."
            self.connected = False
            self.sock.close()
        elif name and not self.userName:
            error = "Error: You are currently unregistered, please register before running any action."

        if error:
            print(error)

        return error
        
    # Fetches a file from the server using a file name
    def fetch_dir(self):
        error = self.check_error(name=True)
        if error:
            return
      
        self.sock.sendall(b"/dir")
        response = ""
        
        while True:
            chunk = self.sock.recv(4096).decode()
            response += chunk
            if len(chunk) < 4096:
                break
        
        response = response.split("|")
        print("Files on server:" + "\n- ".join(["", *response]))

    # Fetches a file from the server using a file name
    def fetch_file(self, filename):
        error = self.check_error(name=True)
        if error:
            return
    
        if not os.path.exists("filedir/" + filename):
            print("Error: File not found in the server.")
            return

        self.sock.sendall(f"/get {filename}".encode())
        fileData = b""

        while True:
            chunk = self.sock.recv(4096)
            fileData += chunk
            if len(chunk) < 4096:
                break

        print("File received from Server: {filename}")
        with open(filename, 'wb') as file:
            file.write(fileData)

    # Sends a file to the server using the current client alias
    def send_file(self, filename):
        error = self.check_error(name=True)
        if error:
            return
    
        if not os.path.exists(filename):
            print("Error: File not found.")
            return

        with open(filename, 'rb') as file:
            fileData = file.read()
            print(fileData)
            self.sock.sendall(f"/store {filename}".encode())
            self.sock.sendall(fileData)

            response = self.sock.recv(1024).decode()
            if response == "SUCCESS":
                time = datetime.now()
                print(f"{self.userName} {time}: Uploaded {filename}")
            else:
                print("Error: Unsuccessful in sending file")

    # registers the User
    def register_alias(self, user):
        error = self.check_error()
        if error:
            return
        
        self.sock.sendall(f"/register {user}".encode())
        response = self.sock.recv(1024).decode()

        if response == "SUCCESS":
            self.userName = user
            print(f"Welcome {self.userName}!")
        else:
            print("Error: Registration failed. Handle or alias already exists.")

    # Disconnects from the current server
    def disconnect(self):
        if not self.connected:
            print("Error: Disconnection failed. Please connect to the server first.")
            return
        
        try:
            self.sock.close()
            self.connected = False
            print("Connection closed. Thank you!")
        except socket.error as e:
            print("Error disconnecting from server.")

    # Connects with the server
    def connect(self):
        if self.connected:
            print("Error: Already connected to a server. Disconnect first to join a new server.")
            return
        
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_IP, self.portNumber))
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

def is_params_valid(expected, observed):
    if expected != observed:
        print("Error: Command parameters do not match or is not allowed.")
        
    return expected == observed

try:
    # Instantiate new client connection
    client = userConnection()

    while True:
        inp = input("> ")
        parsed = inp.split(" ")
        lenParams = len(parsed)

        match parsed[0]:
            case '/join':
                if client.connected:
                    print("Error: You are already connected to a server. Disconnect first to join another one.")
                    continue
                if not is_params_valid(3, lenParams):
                    continue

                client.server_IP = parsed[1]
                client.portNumber = int(parsed[2])
                client.connect()
            case '/leave':
                if not is_params_valid(1, lenParams):
                    continue

                client.disconnect()
            case '/register':
                if not is_params_valid(2, lenParams):
                    continue

                client.register_alias(parsed[1])
            case '/store':
                if not is_params_valid(2, lenParams):
                    continue
                
                client.send_file(parsed[1])
            case '/dir':
                if not is_params_valid(1, lenParams):
                    continue

                client.fetch_dir()
            case '/get':
                if not is_params_valid(2, lenParams):
                    continue

                client.fetch_file(parsed[1])
            case '/?':
                if not is_params_valid(1, lenParams):
                    continue

                client.print_help()
            case '/exit':
                print("See you on the flip side")
                client.disconnect()
                break
            case _:
                print("Error: Command not found")

except KeyboardInterrupt:
    print("Closing client, exiting.")
finally:
    # Close all connections to the server and the server itself
    client.disconnect()