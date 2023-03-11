#server that allows for multiple connections

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

#SET UP LISTENING SOCKET

#host, port = sys.argv[1], int(sys.argv[2])
host = "127.0.0.1"  # Standard loopback interface address (localhost)
port = 65432  # Port to listen on (non-privileged ports are > 1023)

gameList = [] #list of Game classes. 1 for each running game
class Game:
	def __init__(self, firstPlayer, firstPlayerSock):
		self.playerOne = firstPlayer
		self.playerOneSock = firstPlayerSock
	def addSecondPlayer(self, secondPlayer, secondPlayerSock):
		self.playerTwo = secondPlayer
		self.playerTwoSock = secondPlayerSock




def main():
	lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	lsock.bind((host, port)) #associate the socket with a specific network interface and port number
	lsock.listen() #enables server to accept connections. Makes it a "listening" socket. Optional parameter: number of unaccepted connections that the system will allow before refusing new connections
	print(f"Listening on {(host, port)}")
	lsock.setblocking(False) #configures the socket in non-blocking mode
	sel.register(lsock, selectors.EVENT_READ, data=None) #registers the socket to be monitored with sel.select() for the events EVENT_READ

	#EVENT LOOP

	try:
	    while True:
	        events = sel.select(timeout=None) #blocks until there are sockets ready for I/O. 
	        #Returns a list of tuples : (key,mask), one for each socket. 
	        #key: a SelectorKey namedtuple that contains a fileobj attribute. key.fileobj is the socket object.
	        #mask: an event mask of the operations that are ready
	        for key, mask in events:
	            if key.data is None:
	            	#it's from the listening socket and we need to accept the connection.
	                accept_wrapper(key.fileobj) #get the new socket object and register it with the selector
	            else:
	            	#It's a client object that has already been accepted, and we need to service it.
	                service_connection(key, mask)
	except KeyboardInterrupt:
	    print("Caught keyboard interrupt, exiting")
	finally:
	    sel.close()


#Define AcceptWrapper function
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False) #put socket in non-blocking mode
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"") #create an object to hold the data and socket
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data) #pass socket, events mask, and data object to select.register()

#Define ServiceConnection
def service_connection(key, mask):
    sock = key.fileobj #socket object
    data = key.data
    if mask & selectors.EVENT_READ:
    	#Socket is ready for reading
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
        	#if no data is recieved
        	#The client has closed their socket, so the server should too
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            #print(f"Echoing {data.outb!r} to {data.addr}")
       		processInput(data.outb, sock)
        	sent = sock.send(data.outb)  # Should be ready to write. .send() returns number of bytes sent
        	data.outb = data.outb[sent:]

def processInput(dataOut, sock):
	print(sock)
	spec = str(dataOut).split(',')
	print(spec)
	if(spec[1] == "NEW\'"):
		#new game
		print("NEW GAME")
		gameList.append(Game(spec[0], sock))
		print("GAMELIST:")
		print(gameList)
		print(gameList[0].playerOneSock)
	elif(spec[1] == "ACCEPT"):
		pass
		#accept game invitation
	elif(spec[1] == "REJ"):
		pass
		#Reject game invitation

main()








