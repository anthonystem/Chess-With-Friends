import arcade
import arcade.gui
import socket
import time
import threading
import sys
import random

#arcade variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "UI Structure"
SQUARE_SIZE = 100
BOARD_SIZE = 8
MARGIN = 50

#socket variables
HEADER = 64 
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" 
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
clientName = sys.argv[1] #store first command line argument as client name
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setup socket

event = threading.Event()

#method to send message to server
def send(msg, client):
    message = msg.encode(FORMAT) #encode message
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    # print(client.recv(2048).decode(FORMAT))

#waits for input from server and processes input accordingly. Method will be called in new thread as to not stop program executing with infinite while loop
def wait_for_server_input(client):
    while True:
        # msg_length = client.recv(HEADER).decode(FORMAT)
        # if msg_length:
        #     size = int(msg_length)
        #     message = client.recv(size).decode(FORMAT)
        #     msg = message.split(',') #split message into list
        #     if msg[0] == "NEWINVITE":
        #         inv_list.append(msg[1])
                # invitesView.update_list() #CAUSED SEG FAULT
        # msg_length = client.recv(HEADER).decode(FORMAT)
        if event.is_set(): #break if user closes client
            break
        message = client.recv(1024).decode(FORMAT)
        msg = message.split(',') #split message into list
        if msg[0] == DISCONNECT_MESSAGE:
            print("Disconnect Recieved!!!!!")

        if msg[0] == "NEWINVITE": #New invite recieved
            addInviteToInviteDic(msg[1], msg[2]) #arguments: fromPlayer, InviteID
            # invitesView.update_list() #CAUSED SEG FAULT
            
        elif msg[0] == "NEWGAME": #A player accepted your game invitation
            #add game to game list
            print(f"NEW GAME WITH {msg[1]}")
            addGameToGameDic(msg[1], int(msg[2]))
            # currentGamesView.update_list()  #WHY DOES THIS CAUSE A SEG FAULT!!!!!!
    

#Game class
class Game():
    def __init__(self, ID, player1, player2, cont, abort):
        self.id = ID #same id as invite ID
        self.player1 = player1
        self.player2 = player2
        self.cont = cont #continue button
        self.abort = abort #abort button
    def __str__(self): #toString
        return f"Game: {self.player1} vs {self.player2}"

#invite class: ID IS CURRENTLY PLAYER NAME (who sent the invite) INVITES WILL NEED NUMERICAL IDS TO ENSURE THEY ARE UNIQUE
class Invite(): 
    def __init__(self, ID, fromPlayer, acc, rej): #fromPlayer, acceptButton, rejectButton. Doesn't need toPlayer, because that's always the client
        self.id = ID
        self.fromPlayer = fromPlayer
        self.acc = acc #accept button
        self.rej = rej #reject button

#Create new instance of Game class, and add to game dic
def addGameToGameDic(otherPlayer, ID):
    gameToAdd = Game(ID, "You", otherPlayer, ContinueGameButton(text = "Continue", width = 100, height = 20) , RemoveGameButton(text = "Abort", width = 100, height = 20))
    game_dic[gameToAdd.id] = gameToAdd
    print(f"Game id: {gameToAdd.id}")
    # currentGamesView.update_list() #SEG FAULT??!!?!?!?

#Create new invite object, add to player's dic of invites
def addInviteToInviteDic(fromPlayer, inviteID):
    inviteToAdd = Invite(inviteID, fromPlayer, AcceptButton(text = "Accept", width = 100, height = 20), RejectButton(text = "Reject", width = 100, height = 20))
    inv_dic[inviteToAdd.id] = inviteToAdd
    print(f"invite id: {inviteToAdd.id}")
    
#Game List
game_dic = {} #stores instances of game class
#Invites lists
inv_dic = {} #stores instances of invite class

#Buttons
class CurrGamesButton(arcade.gui.UIFlatButton): #takes you to current games screen
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        homeView.manager.disable()
        window.show_view(currentGamesView)
        currentGamesView.manager.enable()
        currentGamesView.update_list()

class InvitesButton(arcade.gui.UIFlatButton): #takes you to invites screen
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        homeView.manager.disable()
        window.show_view(invitesView)
        invitesView.manager.enable()
        invitesView.update_list()
        
class NewGameButton(arcade.gui.UIFlatButton): #takes you to send new game invite screen
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        homeView.manager.disable()
        window.show_view(newGameView)
        newGameView.manager.enable()

class BackHomeButton(arcade.gui.UIFlatButton): #back to home screen
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        window.show_view(homeView)
        homeView.manager.enable()
        invitesView.manager.disable()
        newGameView.manager.disable()
        currentGamesView.manager.disable()

class ContinueGameButton(arcade.gui.UIFlatButton): #continue game. Should take you to board screen
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        pass

class RemoveGameButton(arcade.gui.UIFlatButton): #remove game from game list
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        pass

class AcceptButton(arcade.gui.UIFlatButton): #accept invite
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        for inv in inv_dic:
            if inv_dic[inv].acc is self:
                invToDel = inv #store invite to delete
                #send accepted message to server
                send(f"{clientName},ACCEPT,{inv_dic[inv].id}", client) #FORMAT: ClientName, ACCEPT, InviteID
        del inv_dic[invToDel] #remove key from dic
        #update invite list
        invitesView.update_list()

class RejectButton(arcade.gui.UIFlatButton): #reject invite
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        for inv in inv_dic:
            if inv_dic[inv].rej is self:
                invToDel = inv #store invite to delete
                #update invite list
        send(f"{clientName},REJECT,{inv_dic[inv].id}", client) #FORMAT: ClientName, ACCEPT, InviteID
        del inv_dic[inv]  #remove invite from invite dic
        invitesView.update_list()

class SubmitButton(arcade.gui.UIFlatButton): #Sends new invite to server
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        send(f"{clientName},INVITE,{newGameView.inputInviteText.text}", client)

#Home screen class
class Home(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.csscolor.GRAY)
        self.v_box = arcade.gui.UIBoxLayout(vertical = True, space_between = 10, align = 'left')
        self.curr_games_button = CurrGamesButton(text="View Current Games", width=200)
        self.invites_button = InvitesButton(text="View Game Invites", width=200)
        self.new_game_button = NewGameButton(text="New Game Invite", width=200)
        self.nameLabel = arcade.gui.UILabel(x = 50, y = 750, text = clientName)
        #add each button to vertical stack
        self.v_box.add(self.curr_games_button)
        self.v_box.add(self.invites_button)
        self.v_box.add(self.new_game_button)
        self.v_box.add(self.nameLabel)
        #add vertical stack to manager
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
   
    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.manager.draw()

#current games screen class
class CurrentGames(arcade.View):
    def __init__(self):
        super().__init__()
        #Set up manager and add back button
        self.manager = arcade.gui.UIManager()
        # self.manager.enable()
        self.backButton = BackHomeButton(text="Home", width=100, height = 50, x = 50, y = 700)
        self.manager.add(self.backButton)
        #vertical stack to hold each game
        self.vertStack= arcade.gui.UIBoxLayout(vertical = True, space_between = 10, align = 'left')
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.vertStack)
        )

    #update the list of current games
    def update_list(self):
        self.vertStack.clear() #clear vertical stack
        for game in game_dic:
            gameInfo = arcade.gui.UIBoxLayout(vertical = False, space_between = 10, align = 'right')
            gameInfo.add(arcade.gui.UILabel(text = str(game_dic[game]), font_name = ('Times'), font_size = 20, text_color = (0, 0, 255, 255), bold = True))
            gameInfo.add(game_dic[game].cont)
            gameInfo.add(game_dic[game].abort)
            self.vertStack.add(gameInfo)

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.manager.draw()

#invitations screen class
class Invites(arcade.View):
    def __init__(self):
        super().__init__()
        #Set up manager and add back button
        self.manager = arcade.gui.UIManager()
        # self.manager.enable()
        self.backButton = BackHomeButton(text="Home", width=100, height = 50, x = 50, y = 700)
        self.manager.add(self.backButton)
        #vertival stack to hold each invite
        self.vertStack = arcade.gui.UIBoxLayout(vertical = True, space_between = 10, align = 'left')
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.vertStack)
        )
    
    #update list of invitations
    def update_list(self):
        self.vertStack.clear() #clear vertical stack
        for inv in inv_dic:
            invInfo = arcade.gui.UIBoxLayout(vertical = False, space_between = 10, align = 'right') #create horizontal stack to hold each part of the invite (label, buttons)
            invInfo.add(arcade.gui.UILabel(text = f"Invite from {inv_dic[inv].fromPlayer}", font_name = ('Times'), font_size = 20, text_color = (0, 0, 255, 255), bold = True)) #add invite label
            invInfo.add(inv_dic[inv].acc)
            invInfo.add(inv_dic[inv].rej)
            self.vertStack.add(invInfo) #add invite to vertical stack of all invites

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.manager.draw()

#send new game invite screen class
class NewGame(arcade.View):
    def __init__(self):
        #Set up manager and add back button
        super().__init__()
        self.manager = arcade.gui.UIManager()
        # self.manager.enable()
        self.backButton = BackHomeButton(text="Home", width=100, height = 50, x = 50, y = 700)
        self.manager.add(self.backButton)
        self.inputInviteText = arcade.gui.UIInputText(x = 200, y = 400, text = "Input player name here", width = 250, height = 20)
        self.manager.add(arcade.gui.UIPadding(child = self.inputInviteText, padding = (3,3,3,3), bg_color = (255,255,255)))
        self.manager.add(SubmitButton(text = "Send Invite", x = 500, y = 395, width = 200, height = 30))

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.manager.draw()

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.title = SCREEN_TITLE

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE: #DOESN"T WORK, BECAUSE THREAD IS RUNNING, I THINK. WORKED WITHOUT SOCKET FUNCTIONALITY
            print("ESC")
            event.set()  #stop thread
            send(DISCONNECT_MESSAGE, client) #send disconnect message to server
            arcade.close_window()

#GLOBAL DEFINITIONS
# window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window = GameWindow()
homeView = Home()
currentGamesView = CurrentGames()
invitesView = Invites()
newGameView = NewGame()

def main():

    # socket functionality
    client.connect(ADDR) #connect to server
    send(clientName, client) #send client name to server
    thread = threading.Thread(target = wait_for_server_input, args = [client])
    thread.start()

    #Arcade functionality
    window.show_view(homeView)
    arcade.run()

main()
