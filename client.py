import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def parser(inp):
    return inp.split(' ')

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
    s.close()
    s = socket.socket()

# Connects with the server
def server_connect(host, port):
    s.connect((host, int(port)))
    print(f"Succesfully connected to {host}:{port}!")


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
try:
    while True:
        inp = input("> ")
        print(inp)
        wordList = parser(inp)
        cmd = wordList[0]

        match cmd:
            case '/join':
                server_connect(wordList[1], wordList[2])
            case '/leave':
                server_disconnect()
            case '/register':
                register_alias()
            case '/store':
                send_file(wordList[1])
            case '/dir':
                fetch_dir()
            case '/get':
                fetch_file(wordList[1])
            case '/?':
                print_help()
            case '/exit':
                print("See you on the flip side")
                s.close()
                break

except KeyboardInterrupt:
    print("Closing client, exiting.")
finally:
    # Close all connections to the server and the server itself
    s.close()