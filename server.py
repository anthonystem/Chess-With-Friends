import socket
import threading
import time
import random
import json
import string
import pymysql
from database import *

connection = pymysql.connect(
	host = "chesswithfriends.cwqryofoppjg.us-east-2.rds.amazonaws.com",
	port = 3306,
	user = "admin",
	password = "password",
	db = "chesswithfriends"
)

cursor = connection.cursor()

# print(selectTableFields("tblGameInvites",cursor))

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" 

def send(msg, sock):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	try:
		sock.send(send_length)
		# print(f"sent {send_length}")
		sock.send(message)
		# print(f"sent {message}")
	except:
		print("CLIENT NOT CONNECTED")

playerDic = {} #dictionary of player classes. Key = playerName (identifying key). Value = player object

class Player:
	def __init__(self, name, sock):
		self.name = name #name string
		self.sock = sock #socket object
		self.connected = True
		self.games = {} #Dictionary of current games. key = id, value = game object
		self.invitesRecieved = {} #dictionary of invites they have recieved. key = id, value = invite object

class Square():
    def __init__(self, xCoord, yCoord, x, y):
        self.x = x
        self.y = y

class Piece():
    def __init__(self, color, type, square):
        self.color = color
        self.type = type
        self.hasMoved = False
        self.location = square

class Game:
	def __init__(self, ID, firstPlayer, secondPlayer, colorChoice):
		self.id = ID
		#set players, according to color choice
		if colorChoice == "white":
			print("white")
			self.player1 = firstPlayer #player object. access name with self.player1.name. player1 = white, player2 = black
			self.player2 = secondPlayer
		elif colorChoice == "black":
			print("black")
			self.player2 = firstPlayer
			self.player1 = secondPlayer
		elif colorChoice == "random":
			print("random")
			rand = random.randint(0,1)
			if rand == 1:
				self.player1 = firstPlayer
				self.player2 = secondPlayer
			else:
				self.player2 = firstPlayer
				self.player1 = secondPlayer
		self.turn = "white"
		self.pieces = {}
		self.jsonState = None

class Invite:
	def __init__(self, fromPlayer, toPlayer, colorChoice):
		self.id = random.randint(0,1000) #generate random ID
		self.fromPlayer = fromPlayer #player object. access name with self.fromPlayer.name
		self.toPlayer = toPlayer
		self.colorChoice = colorChoice

#given player object and game ID, returns other player object
def getOtherPlayer(player, ID):
	if player.games[ID].player1 is player:
		return player.games[ID].player2
	else:
		return player.games[ID].player1

def addGame(player, ID):
	player1 = playerDic[player].invitesRecieved[ID].fromPlayer
	player2 = playerDic[player].invitesRecieved[ID].toPlayer
	game = Game(ID, player1, player2, playerDic[player].invitesRecieved[ID].colorChoice) #create game object
	player1.games[game.id] = game #add game object to gameList for each player. Both values in player game dic reference the same game
	player2.games[game.id] = game
	return game.id

#create new invite object and add to toPlayer's list of recieved invites
#return invite ID (randomly generated)
def addInvite(fromPlayer, toPlayer, colorChoice): #pass in names as strings
	# fromPlayerObj = playerDic[fromPlayer]
	# toPlayerObj = playerDic[toPlayer]
	# invite = Invite(fromPlayerObj, toPlayerObj, colorChoice)
	# toPlayerObj.invitesRecieved[invite.id] = invite #add invite to recieving player's invitesRecieved

	#add invite to database
	inviteID = insertNewGameInvite(fromPlayer, toPlayer, colorChoice, cursor, connection)
	#retrieve invite info
	inviteInfo = selectGameInviteByID(inviteID,cursor)

	# return invite.id
	return inviteInfo

#remove invite from player's list of invites
def removeInvite(ID, toPlayer):
	toPlayer = playerDic[toPlayer]
	del toPlayer.invitesRecieved[ID]

#call addInvite
#send invite to recieving player
def invitePlayer(spec):
	#check if player is a real player
	if verifyUser(spec[2], cursor):
		# inviteID = addInvite(spec[0], spec[2], spec[3]) #add invite to player's dic of invites
		# # playerDic[spec[2]].sock.send(f"NEWINVITE,{str(spec[0])},{str(inviteID)}".encode(FORMAT)) #send player the invite. FORMAT: NEWINVITE, FromPlayer, InviteID
		# send(f"NEWINVITE,{str(spec[0])},{str(inviteID)}", playerDic[spec[2]].sock)
		inviteInfo = addInvite(spec[0], spec[2], spec[3])
		ID = inviteInfo[0]
		fromPlayer = inviteInfo[1]
		toPlayer = inviteInfo[2]
		#send to recieving player
		if toPlayer in playerDic:
			connected = playerDic[toPlayer].connected
			if connected:
				send(f"NEWINVITE,{fromPlayer},{ID}",playerDic[toPlayer].sock)
	else:
		pass #invalid invite

def acceptInvite(spec):
	player = spec[0]
	ID = int(spec[2])
	updateAcceptInvite(ID,cursor,connection)

	#add game to each player's dic of games. Arguments: playerName, inviteID
	# addGame(player, ID)
	#remove invite
	# removeInvite(ID, player) #INVITE WAS TO "player"
	#send both players the game
	# game = playerDic[player].games[ID]
	# print(f"Game ID: {game.id}")
	# p1 = game.player1 #player that initially sent the invite
	# p2 = game.player2 #player that accepted the invite
	# p1.sock.send(f"NEWGAME,{p2.name}, {str(ID)},white".encode(FORMAT)) #FORMAT: INVITEACCEPTED, OtherPlayer, ID, color
	# p2.sock.send(f"NEWGAME,{p1.name}, {str(ID)},black".encode(FORMAT))
	# send(f"NEWGAME,{p2.name}, {str(ID)},white,{p2.connected}",p1.sock)
	# send(f"NEWGAME,{p1.name}, {str(ID)},black,{p1.connected}",p2.sock)

def rejectInvite(spec):
	player = spec[0]
	ID = int(spec[2])
	updateRejectInvite(ID,cursor,connection)
	# removeInvite(ID, player) #INVITE WAS TO "player"

def abortGame(spec):
	p1 = playerDic[spec[0]] #player that resigned
	ID = int(spec[2])
	p2 = getOtherPlayer(p1,ID) #player that won

	gameToRemove = p1.games[ID]
	# p1 = gameToRemove.player1
	# p2 = gameToRemove.player2
	#Remove game from both players' game dicts
	del p1.games[gameToRemove.id]
	del p2.games[gameToRemove.id]
	#send game removal to both players
	# p1.sock.send(f"DELGAME,{str(gameToRemove.id)}".encode(FORMAT)) #FORMAT: DELGAME, GameID
	# p2.sock.send(f"DELGAME,{str(gameToRemove.id)}".encode(FORMAT))
	send(f"RESIGNLOSS,{str(gameToRemove.id)}",p1.sock)
	send(f"RESIGNWIN,{str(gameToRemove.id)}",p2.sock)

def movePiece(spec, msgStr):
	#spec: [movingPlayerName, MOVE, jsonString (but split up every comma, so not really)]
	#TODO: Update game state on server
	#Send to client
	sendingPlayer = spec[0]
	ind = str(msgStr).index("{")
	jsonStr = msgStr[int(ind):]
	gameObj = json.loads(jsonStr)
	recievingPlayer = playerDic[gameObj["player2"]]
	ID = gameObj["id"]
	#Store game state in server
	recievingPlayer.games[ID].pieces = gameObj['pieces'] #only need to update for one player, since both game dict values point to the same game object
	recievingPlayer.games[ID].turn = gameObj['turn']
	recievingPlayer.games[ID].jsonState = jsonStr
	#send to other player
	# recievingPlayer.sock.send(f"NEWMOVE,{ID},{jsonStr}".encode(FORMAT)) #FORMAT: NEWMOVE, ID, jsonString
	send(f"NEWMOVE,{ID},{jsonStr}",recievingPlayer.sock)

def endGame(spec):
	player = playerDic[spec[0]]
	ID = int(spec[2])
	game = player.games[ID]
	if spec[3] == "black":
		winner = game.player1
		loser = game.player2
	else:
		winner = game.player2
		loser = game.player1
	#send checkmate message to each player
	send(f"WIN,{str(ID)}",winner.sock)
	send(f"LOSE,{str(ID)}",loser.sock)

#update player's client with invites and games upon reconnecting to server
def updateOnReconnect(playerName):
	player = playerDic[playerName]
	#update games
	# for game in player.games:
	# 	ID = player.games[game].id #Get game ID
	# 	#Get other player
	# 	if player.games[game].player1 is player: #player is player1
	# 		otherPlayer = player.games[game].player2
	# 		color = "white"
	# 	else: #player is player2
	# 		otherPlayer = player.games[game].player1
	# 		color = "black"
	# 	#Send game to player
	# 	# player.sock.send(f"NEWGAME,{otherPlayer.name}, {str(ID)},{color}".encode(FORMAT)) #FORMAT: INVITEACCEPTED, OtherPlayer, ID, color
	# 	send(f"NEWGAME,{otherPlayer.name}, {str(ID)},{color},{otherPlayer.connected}",player.sock)
	# 	# player.sock.send(f"SETGAME, {player.games[ID].jsonState}".encode(FORMAT))
	# 	send(f"SETGAME, {player.games[ID].jsonState}",player.sock)
	# 	time.sleep(.1)
	#update invites
	# for inv in player.invitesRecieved:
	# 	print(f"sent player invite {inv} on reconnect")
	# 	# player.sock.send(f"NEWINVITE,{player.invitesRecieved[inv].fromPlayer.name},{str(inv)}".encode(FORMAT)) #send player the invite. FORMAT: NEWINVITE, FromPlayer, InviteID
	# 	send(f"NEWINVITE,{player.invitesRecieved[inv].fromPlayer.name},{str(inv)}", player.sock)
	# 	time.sleep(.1)

	invites = selectIncomingGameInvites(playerName,cursor)
	for inv in invites:
		ID = inv[0]
		fromPlayerName = inv[1]
		send(f"NEWINVITE,{fromPlayerName},{ID}", player.sock)


def notifyDisconnect(playerName):
	player = playerDic[playerName]
	player.connected = False
	for game in player.games:
		otherPlayer = getOtherPlayer(player,game)
		send(f"DISC,{game}",otherPlayer.sock)

def checkLogin(username,password,sock):
	# print(username)
	# print(password)
	#verify login
	validLogin = verifyPassword(username.rstrip(),password.rstrip(),cursor)
	
	if validLogin:
		if username not in playerDic: #if new player
			playerDic[username] = Player(username,sock) #add player to player dic
		elif username in playerDic: #if player is reconnecting
			playerDic[username].sock = sock #update socket
		
		updateOnReconnect(username) 	#send player invites and current games
		playerDic[username].connected = True
		#send back to player
		send(f"VALIDLOGIN,{username}",sock)
	else:
		send(f"INVALIDLOGIN,{username}",sock)

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
			spec = msg.split(',')
			if spec[0] == DISCONNECT_MESSAGE:
				connected = False
				print(f"{addr} ({spec[1]}) Disconected")
				# conn.send(DISCONNECT_MESSAGE.encode(FORMAT))
				send(DISCONNECT_MESSAGE, conn)
				notifyDisconnect(spec[1])
			elif spec[0] == "LOGIN":
				checkLogin(spec[1].rstrip(),spec[2].rstrip(),conn)
			else:
				# print(f"[{addr}] {msg}")
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
	# if len(spec) == 1: #TRUE IF PLAYER HAS JUST OPENED CLIENT. THIS SECTION WILL BE REPLACED BY CHECK LOGIN METHOD
	# 	if spec[0] not in playerDic: #if new player
	# 		playerDic[spec[0]] = Player(spec[0],sock) #add player to player dic
	# 	elif spec[0] in playerDic: #if player is reconnecting
	# 		playerDic[spec[0]].sock = sock #update socket
	# 		updateOnReconnect(spec[0]) 	#send player invites and current games
	# 		playerDic[spec[0]].connected = True
	
	if(len(spec)>1):
		#client is sending a new game invitation
		if(spec[1] == "INVITE"):
			# if spec[2] not in playerDic: #invalid invite - player not in system
			# 	# sock.send("Invited player is not in the system".encode(FORMAT))
			# 	pass
			# elif spec[2] == spec[0]: #invalid invite - player tried to invite themselves
			# 	pass
			# else:#invite is valid - send invite
			# 	invitePlayer(spec)
			invitePlayer(spec)

		#Client accepted game invite
		elif(spec[1] == "ACCEPT"):
			acceptInvite(spec)

		#client rejected game invitation
		elif(spec[1] == "REJECT"):
			rejectInvite(spec)

		elif(spec[1] == "ABORT"):
			abortGame(spec)

		elif(spec[1] == "MOVE"):
			movePiece(spec, msg)
		
		elif(spec[1] == "MATE"):
			endGame(spec)


def main():
	print("STARTING server")
	start()

main()