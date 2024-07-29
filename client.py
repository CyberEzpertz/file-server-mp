import socket
import os
import selectors
import sys, time, signal
import threading
from datetime import datetime

class userConnection:
    def __init__(self):
        self.userName = None
        self.connected = False
        self.server_IP = None
        self.portNumber = None
        self.sock = None
        self.chat = False
        self.exit = False

    def check_error(self, connection=True, name=False):
        error = None
        if connection and not self.connected:
            error = "Error: Not currently connected to a server."
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

        print(f"File received from Server: {filename}")
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
            self.sock.sendall(f"/store {filename}".encode())
            response = self.sock.recv(1024).decode()

            if response == "SEND":
                self.sock.sendall(fileData)
            else:
                print("Error: Unsuccessful in sending file")

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
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.userName = None
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

    def toggle_chat(self):
        self.chat = not self.chat
        self.sock.sendall("/chat")

    def broadcast(self, message):
        error = self.check_error(name=True)
        if error:
            return
        
        self.sock.sendall(f"/broadcast {message}".encode())

    def whisper(self, username, message):
        error = self.check_error(name=True)
        if error:
            return
        
        self.sock.sendall(f"/whisper {username} {message}".encode())
        response = self.sock.recv(1024).decode()

        if response == "SUCCESS":
            print(f"Whispered to {username}: {message}")
        else:
            print(response)
        
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

# Instantiate new client connection
client = userConnection()

# We need this for the multithreading to exit properly
exitFlag = False

def command_func():
    while not exitFlag:
        try:
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
                case '/broadcast':
                    client.broadcast(parsed[1])
                case '/whisper':
                    if parsed[1] == client.userName:
                        print("You can't whisper to yourself!")
                    else:
                        client.whisper(parsed[1], parsed[2])
                case _:
                    print("Error: Command not found")
        except Exception as e:
            if(client.connected):
                client.disconnect()
            break

def chat_func():
    while not exitFlag:
        try:
            if(client.connected):
                message = client.sock.recv(1024, socket.MSG_PEEK).decode()
                if message.startswith("<"):
                    message = client.sock.recv(1024).decode()
                    print(message + "\n> ", end="")
        except:
            break

chat_thread = threading.Thread(target=chat_func)
chat_thread.start()

command_thread = threading.Thread(target=command_func)
command_thread.start()

try:
    while chat_thread.is_alive() or command_thread.is_alive():
        time.sleep(1)
except KeyboardInterrupt:
    exitFlag = True
    command_thread.join()
    chat_thread.join()

print("Goodbye!")