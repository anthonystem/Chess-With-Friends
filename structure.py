import arcade
import arcade.gui
import socket
import time
import threading
import sys

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
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            size = int(msg_length)
            message = client.recv(size).decode(FORMAT)
            msg = message.split(',') #split message into list
            if msg[0] == "NEWINVITE":
                inv_list.append(msg[1])
                # invitesView.update_list()

#Game class
class Game():
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
    def __str__(self):
        return f"Game: {self.player1} vs {self.player2}"
    
#Game List
game_list = []

#Invites lists
inv_list = [] #stores invitations before they are created as an instance of the invite class. Used to address a wierd seg fault
inv_class_list = [] #stores instances of invite class

#invite class 
class Invite():
    def __init__(self, id, acc, rej):
        self.id = id
        self.acc = acc
        self.rej = rej

#Buttons
class CurrGamesButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        homeView.manager.disable()
        window.show_view(currentGamesView)
        currentGamesView.manager.enable()

class InvitesButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        homeView.manager.disable()
        window.show_view(invitesView)
        invitesView.manager.enable()
        invitesView.update_list()
        
class NewGameButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        homeView.manager.disable()
        window.show_view(newGameView)
        newGameView.manager.enable()

class BackHomeButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        window.show_view(homeView)
        homeView.manager.enable()
        invitesView.manager.disable()
        newGameView.manager.disable()
        currentGamesView.manager.disable()

class ContinueGameButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        pass

class RemoveGameButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        pass

class AcceptButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        for invite in inv_class_list:
            if invite.acc is self:
                # add game to game list
                game_list.append(Game("You",str(invite.id)))
                #update game list
                currentGamesView.update_list()
                #remove invite from both invite lists
                inv_class_list.remove(invite)
                inv_list.remove(invite.id)
                #update invite list
                invitesView.update_list()

                

class RejectButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        for invite in inv_class_list:
            if invite.rej is self:
                #remove invite from both invite lists
                inv_class_list.remove(invite)
                inv_list.remove(invite.id)
                #update invite list
                invitesView.update_list()

class SubmitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        print("1")
        send(f"{clientName},INVITE,{newGameView.inputInviteText.text}", client)
        print("2")

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
        #add each button to vertical stack
        self.v_box.add(self.curr_games_button)
        self.v_box.add(self.invites_button)
        self.v_box.add(self.new_game_button)
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
        self.manager.enable()
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
        for game in game_list:
            gameInfo = arcade.gui.UIBoxLayout(vertical = False, space_between = 10, align = 'right')
            gameInfo.add(arcade.gui.UILabel(text = str(game), font_name = ('Times'), font_size = 20, text_color = (0, 0, 255, 255), bold = True))
            gameInfo.add(ContinueGameButton(text = "Continue", width = 100, height = 20))
            gameInfo.add(RemoveGameButton(text = "Abort", width = 100, height = 20))
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
        self.manager.enable()
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
        for inv in inv_list:
            invInfo = arcade.gui.UIBoxLayout(vertical = False, space_between = 10, align = 'right') #create horizontal stack to hold each part of the invite (label, buttons)
            invInfo.add(arcade.gui.UILabel(text = f"Invite from {inv}", font_name = ('Times'), font_size = 20, text_color = (0, 0, 255, 255), bold = True)) #add invite label
            invite = Invite(inv, AcceptButton(text = "Accept", width = 100, height = 20), RejectButton(text = "Reject", width = 100, height = 20)) #create instance of Invite class
            invInfo.add(invite.acc) #add accept button
            invInfo.add(invite.rej) #add reject button
            self.vertStack.add(invInfo) #add invite to vertical stack of all invites
            inv_class_list.append(invite) #add Invite object to list of Invites

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
        self.manager.enable()
        self.backButton = BackHomeButton(text="Home", width=100, height = 50, x = 50, y = 700)
        self.manager.add(self.backButton)
        self.inputInviteText = arcade.gui.UIInputText(x = 200, y = 400, text = "Input player name here", width = 250, height = 20)
        self.manager.add(arcade.gui.UIPadding(child = self.inputInviteText, padding = (3,3,3,3), bg_color = (255,255,255)))
        self.manager.add(SubmitButton(text = "Send Invite", x = 500, y = 395, width = 200, height = 30))
        

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.manager.draw()

#GLOBAL DEFINITIONS
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
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
