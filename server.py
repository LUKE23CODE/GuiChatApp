import socket
from threading import Thread

# Server's IP Address
SERVER_HOST = "0.0.0.0"  # My IP Address "160.0.193.103"
SERVER_PORT = 5002  # port we want to use

# we will use this to separate the client name & message
seperator_token = "<SEP>"

# Initialize list/set of all connected client's sockets
client_sockets = set()

# create a TCP socket
s = socket.socket()

# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))

# listen for upcoming connections
s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """

    while True:
        try:
            # keep listening for a message from "cs" socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            msg = msg.replace(seperator_token, ": ")

        for client_socket in client_sockets:
            client_socket.send(msg.encode())


while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()

for cs in client_sockets:
    cs.close()

s.close()
