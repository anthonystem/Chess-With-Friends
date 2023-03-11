import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #Creates a socket object that supports the context manager type (can be used in a "with" statement). Arguments are constants specifying address family (IPv4) and socket type (TCP).
    s.bind((HOST, PORT)) #associate the socket with a specific network interface and port number
    s.listen() #enables server to accept connections. Makes it a "listening" socket. Optional parameter: number of unaccepted connections that the system will allow before refusing new connections
    conn, addr = s.accept() #blocks execution and waits for incoming connection. When a client connects, it returns a new socket object representing the connection and a tuple [(host,port) for IPv4] holding the address of the client. 
    #accept() creates a new socket object. This is the socket that we'll use to communicate with the client. Separate from the listening socket that the server uses to accept new connections.
    with conn:
        print(f"Connected by {addr}")
        while True: #loops over blocking calls to conn.recv()
            data = conn.recv(1024)
            if not data:
                break
            response = bytes(str(int(data) * 5), 'utf-8')
            conn.sendall(response) #sends data back
