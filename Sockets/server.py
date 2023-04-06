import socket
import threading
import time
import random

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" 

playerDic = {} #dictionary of player classes. Key = playerName (identifying key). Value = player object

class Player:
	def __init__(self, name, sock):
		self.name = name #name string
		self.sock = sock #socket object
		self.connected = True
		self.games = {} #Dictionary of current games. key = id, value = game object
		self.invitesRecieved = {} #dictionary of invites they have recieved. key = id, value = invite object

class Game:
	def __init__(self, firstPlayer, secondPlayer):
		self.id = random.randint(0,1000)
		self.playerOne = firstPlayer #player object. access name with self.playerOne.name
		self.playerTwo = secondPlayer
		self.board = None

class Invite:
	def __init__(self, fromPlayer, toPlayer):
		self.id = random.randint(0,1000)
		self.fromPlayer = fromPlayer #player object. access name with self.fromPlayer.name
		self.toPlayer = toPlayer

def addGame(player1, player2): #pass in names as strings
	player1 = playerDic[player1] #Make player variables references to player objects
	player2 = playerDic[player2] 
	game = Game(player1, player2) #create game object
	player1.games[game.id] = game #add game object to gameList for each player. Both values in player game dic reference the same game
	player2.games[game.id] = game

def addInvite(fromPlayer, toPlayer): #pass in names as strings
	fromPlayer = playerDic[fromPlayer] 
	toPlayer = playerDic[toPlayer]
	invite = Invite(fromPlayer, toPlayer)
	toPlayer.invitesRecieved[invite.id] = invite #add invite to recieving player's invitesRecieved

def updateOnReconnect(playerName):
	player = playerDic[playerName]
	#update games
	for game in player.games:
		if game.playerOne is player:
			player.sock.send(f"INVITEACCEPTED,{game.playerTwo}".encode(FORMAT)) #FOR NOW, DON'T NEED NEW MESSAGE FOR UPDATING GAMES ON RECONNECT. INVITEDACCEPTED WORKS FINE
		else:
			player.sock.send(f"INVITEACCEPTED,{game.playerOne}".encode(FORMAT))
	#update invites
	for invite in player.invitesRecieved:
		player.sock.send(f"NEWINVITE,{invite.fromPlayer.name}".encode(FORMAT))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #choose socket family and type
server.bind(ADDR) #bind server to address

#send
# def send(msg, client):
#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     client.send(send_length)
#     client.send(message)
#     print(client.recv(2048).decode(FORMAT))

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
				# conn.send("Disconnect Recieved\n".encode(FORMAT))
			else:
				print(f"[{addr}] {msg}")
				# conn.send("Message recieved\n".encode(FORMAT))
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
	if len(spec) == 1: #TRUE IF PLAYER HAS JUST OPENED CLIENT
		if spec[0] not in playerDic: #if new player
			playerDic[spec[0]] = Player(spec[0],sock) #add player to player dic
		elif spec[0] in playerDic: #if player is reconnecting
			playerDic[spec[0]].sock = sock #update socket
			updateOnReconnect(spec[0]) 	#send player invites and current games
	
	elif(len(spec)>1):
		#New game invitation
		if(spec[1] == "INVITE"):

			if spec[2] not in playerDic: #invalid invite - player not in system
				# sock.send("Invited player is not in the system".encode(FORMAT))
				pass
			else: #invite is valid - send invite
				invitePlayer(spec)

		#Accept game invite
		elif(spec[1] == "ACCEPT"):
			acceptInvite(spec)

		#reject game invitation
		elif(spec[1] == "REJECT"):
			rejectInvite(spec)


def invitePlayer(spec):
	# playerDic[spec[0]].sock.send("Game invitation sent".encode(FORMAT))
	# print(playerDic[spec[2]].name)
	playerDic[spec[2]].sock.send(f"NEWINVITE,{str(spec[0])}".encode(FORMAT))
	# send(f"NEWINVITE,{str(spec[0])}", playerDic[spec[2]].sock)

def acceptInvite(spec):
	# playerDic[spec[2]].sock.send(f"{spec[0]} accepted your game invite.".encode(FORMAT))
	# gameList.append(Game(spec[2],spec[0])) #add game to gameList
	# print("GAMELIST:")
	# print(gameList.playerOne)
	# print(gameList.playerTwo)
	playerDic[spec[2]].sock.send(f"INVITEACCEPTED,{str(spec[0])}".encode(FORMAT))


def rejectInvite(spec):
	# playerDic[spec[2]].sock.send(f"{spec[0]} rejected your game invite.".encode(FORMAT))
	pass

def main():
	print("STARTING server")
	start()

main()