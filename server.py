import socket
import threading
import time

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT) 
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" 

gameList = [] #list of Game classes. 1 for each running game

playerDic = {} #dictionary of player classes. Key = playerName. Value = player object

class Player:
	def __init__(self, name, sock):
		self.name = name
		self.sock = sock
		self.connected = True

class Game:
	def __init__(self, firstPlayer, secondPlayer):
		self.playerOne = firstPlayer
		self.playerTwo = secondPlayer

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #choose socket family and type
server.bind(ADDR) #bind server to address

#handles individual connection between client and server
def handle_client(conn, addr):
	print(f"[NEW CONNECTION] {addr} connected.")
	connected = True
	while connected:
		msg_length = conn.recv(HEADER).decode(FORMAT) # recv blocks until message from client is recieved.
		if msg_length: #if there is a message. True if not first time connecting
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT) 
			if msg == DISCONNECT_MESSAGE:
				connected = False
				print("Disconected")
			else:
				print(f"[{addr}] {msg}")
				conn.send("Message recieved".encode(FORMAT))
				process(conn, msg)
	
	conn.close() #close current connection after client has disconnected

#handle new connections
def start():
	server.listen() #listen for new connections
	print(f"Server is listening on {SERVER}")
	while True:
		conn, addr = server.accept() #blocks - waits for a new connection to server. When new connection occurs, store socket object (conn) and address (addr)
		#start new thread
		thread = threading.Thread(target = handle_client, args = (conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def process(sock, msg): #socket object, message
	spec = msg.split(',') #split string message into list
	#process appropriately
	if len(spec) == 1: 
		if spec[0] not in playerDic: #add player to player dic if not already in it
			playerDic[spec[0]] = Player(spec[0],sock)
		elif spec[0] in playerDic: #update player socket if player is reconnecting
			playerDic[spec[0]].sock = sock
			playerDic[spec[0]].sock.send("Updated Connection".encode(FORMAT))
	
	elif(len(spec)>1):

		#New game invitation
		if(spec[1] == "INVITE"):

			if spec[2] not in playerDic: #invalid invite - player not in system
				sock.send("Invited player is not in the system".encode(FORMAT))
			else: #invite is valid - send invite
				invitePlayer(spec)

		#Accept game invite
		elif(spec[1] == "ACCEPT"):
			acceptInvite(spec)

		#reject game invitation
		elif(spec[1] == "REJECT"):
			rejectInvite(spec)


def invitePlayer(spec):
	playerDic[spec[0]].sock.send("Game invitation sent".encode(FORMAT))
	print(playerDic[spec[2]].name)
	playerDic[spec[2]].sock.send(("Recieved game invitation from " + str(spec[0])).encode(FORMAT))

def acceptInvite(spec):
	playerDic[spec[2]].sock.send(f"{spec[0]} accepted your game invite.".encode(FORMAT))
	gameList.append(Game(spec[2],spec[0])) #add game to gameList
	print("GAMELIST:")
	print(gameList.playerOne)
	print(gameList.playerTwo)


def rejectInvite(spec):
	playerDic[spec[2]].sock.send(f"{spec[0]} rejected your game invite.".encode(FORMAT))

def main():
	print("STARTING server")
	start()

main()