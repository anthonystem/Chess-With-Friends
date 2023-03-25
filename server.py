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
	spec = msg.split(',')
	#print(spec)

	#add player to player dic if not already in it
	if spec[0] not in playerDic:
		playerDic[spec[0]] = Player(spec[0],sock)
	
	if(len(spec)>1):
		#New game
		if(spec[1] == "INVITE"):
			#print("GAME INVITATION")
			#gameList.append(Game(spec[0], sock))
			#print("GAMELIST:")
			#print(gameList)
			#time.sleep(7)
			#gameList[0].playerOneSock.send("HERERERE".encode(FORMAT))

			if spec[2] not in playerDic: #invalid invite
				sock.send("Invited player is not in the system".encode(FORMAT))
			else:
				invitePlayer(spec[0],spec[2])


		#Accept game invite
		elif(spec[1] == "ACCEPT"):
			pass

		#reject game invitation
		elif(spec[1] == "REJ"):
			pass
			#Reject game invitation

def invitePlayer(player1, player2):
	playerDic[player1].sock.send("Game invitation sent".encode(FORMAT))
	playerDic[player2].sock.send(("Recieved game invitation from " + str(player1)).encode(FORMAT))

def main():
	print("STARTING server")
	start()

main()