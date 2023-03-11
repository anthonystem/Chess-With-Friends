import sys
import socket
import selectors
import types


host = "127.0.0.1"  # The server's hostname or IP address
port = 65432  # The port used by the server

sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]

def main():
    s = start_connections(host,port,1)
    userInput = input("ENTER INPUT HERE: ")
    s.sendall(bytes(userInput, 'utf-8'))
    data = s.recv(1024)
    print(f"RECIEVED {data!r}")


def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns): #num_cons is read from the command line and is the number of connections to create to the server
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)
    return(sock)

main()