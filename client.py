import socket

# Fetches a file from the server using a file name
def fetch_dir():
    pass

# Fetches a file from the server using a file name
def fetch_file(filename):
    pass

# Sends a file to the server using the current client alias
def send_file(filename):
    pass

# Disconnects from the current server
def register_alias():
    pass

# Disconnects from the current server
def server_disconnect():
    pass

# Connects with the server
def server_connect():
    pass

# Prints the commands and their functions
def print_help():
    pass

s = socket.socket()

# Ask for input while client is open
while True:
    inp = input("$ ")
    print(inp)