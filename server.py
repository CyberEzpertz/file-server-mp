import socket
import selectors
import types

def register_client(sock):
    conn, addr = sock.accept()
    print(f"Connection accepted from: {addr}")

    # This will allow for other socket operations to happen while a client is connected
    conn.setblocking(False)

    # This line is to simply store the data associated with the client
    data = types.SimpleNamespace(addr=addr, inb=b"", outb="", handle=None)

    # This line is to check for read or write events from the client
    events = selectors.EVENT_READ | selectors.EVENT_WRITE

    # Register it as part of the selector, which is basically the list of connections/sockets
    sel.register(conn, events, data=data)

def handle_event():
    pass
# To enable multiple clients to connect to the server
sel = selectors.DefaultSelector()

# Initialize the server socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port  = socket.gethostname(), 12345

# Open up the server socket for incoming connections
s.bind((host, port))
s.listen()
s.setblocking(False)
print(f"Server listening on: {host}:{port}")

# Add the listening socket to the selectors, which is the list of sockets
sel.register(s, selectors.EVENT_READ, data=None)

# Loop while the server is on
try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                register_client(key.fileobj)
            else:
                handle_event()
except KeyboardInterrupt:
    print("Closing server, exiting.")
finally:
    # Close all connections to the server and the server itself
    sel.close()