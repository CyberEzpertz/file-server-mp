import socket
import selectors
import types
import os

def is_handle_taken(name):
    for key in sel.get_map().values():
        if key is not None and key.data is not None and key.data.handle == name:
            return True
    
    return False

def register_client(sock):
    conn, addr = sock.accept()
    print(f"Connection accepted from: {addr}")

    # This will allow for other socket operations to happen while a client is connected
    conn.setblocking(False)

    # This line is to simply store the data associated with the client
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", handle=None, file="")

    # This line is to check for read or write events from the client
    events = selectors.EVENT_READ | selectors.EVENT_WRITE

    # Register it as part of the selector, which is basically the list of connections/sockets
    sel.register(conn, events, data=data)

def write_file(data):
    filename = "filedir/" + data.file

    # Write into the file
    with open(filename, "w") as file:
        file.write(data.inb.decode())
        
        print("Closing File...")
        file.close()

    # Reset the filename for the client
    if not data.inb:
        data.file = ""

def handle_event(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        # Get data from the client
        received = sock.recv(1024)
        if received and data.file:
            data.inb += received
        elif received:
            print("reading")
            parsed = received.decode().split(" ")

            match parsed[0]:
                case "/dir":
                    files = os.listdir("./filedir")
                    data.outb = str.encode("|".join(files))
                case "/register":
                    handle = parsed[1]
                    if is_handle_taken(handle):
                        data.outb = b"ERROR"
                    else:
                        data.handle = handle
                        data.outb = b"SUCCESS"
                case "/store":
                    data.file = parsed[1]
                case "/get":
                    
                    pass
        else:
            print(f"Closing connection from {data.addr}")
            sel.unregister(sock)
            sock.close()
    
    # Check if socket is ready to write to and there's data to be sent
    if (mask & selectors.EVENT_WRITE) and data.outb:
        print(f"Sending {data.outb!r} to {data.addr}")
        sent_bytes = sock.send(data.outb)
        data.outb = data.outb[sent_bytes:]

    if (mask & selectors.EVENT_WRITE) and data.inb:
        try:
            write_file(data)
            sock.sendall(b"SUCCESS")
        except:
            sock.sendall(b"ERROR")

# To enable multiple clients to connect to the server
sel = selectors.DefaultSelector()

# Initialize the server socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port  = socket.gethostname(), 12345

# Open up the server socket for incoming connections
s.bind((host, port))
s.listen()
s.setblocking(False)

# Add the listening socket to the selectors, which is the list of sockets
sel.register(s, selectors.EVENT_READ, data=None)

# Loop while the server is on
try:
    idle = False
    print(f"Server listening on: {host}:{port}")

    while not idle:
        # Listen for 60 seconds only
        events = sel.select(timeout=10)
        if not events:
            idle = True
            
            while idle:
                user = input("> Server currently idle, type 'quit' to quit or 'listen' to continue\n")
                match user:
                    case "quit":
                        print("Closing server.")
                        sel.close()
                        break
                    case "listen":
                        idle = False
                    case _:
                        print("Invalid input.")
        else:
            for key, mask in events:
                # If data is None, we know this is from the listening socket because data=None
                if key.data is None:
                    register_client(key.fileobj)
                else:
                    handle_event(key, mask)

except KeyboardInterrupt:
    print("Closing server.")
finally:
    # Close all connections to the server and the server itself
    sel.close()