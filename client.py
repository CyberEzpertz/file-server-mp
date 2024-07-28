import socket

def parser(inp):
    wordList = inp.split(' ')
    commandWord = wordList[0]
    newWord = commandWord[1:]
    wordList[0] = newWord
    return wordList

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

s = socket.socket()

# Ask for input while client is open
while True:
    inp = input("> ")
    print(inp)
    wordList = parser(inp)
    commandWord = wordList[0]
    if commandWord == 'join':
        server_connect()
    elif commandWord == 'leave':
        server_disconnect()
    elif commandWord == 'register':
        register_alias()
    elif commandWord == 'store':
        send_file(wordList[1])
    elif commandWord == 'dir':
        fetch_dir()
    elif commandWord == 'get':
        fetch_file(wordList[1])
    elif commandWord == '?':
        print_help()

    if wordList[0] == "exit":
        print("See you on the flip side")
        break