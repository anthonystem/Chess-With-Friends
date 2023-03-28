import arcade
import arcade.gui
import socket
import time
import threading
import sys

#arcade variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "UI Test"
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
clientName = sys.argv[1]
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setup socket


#socket function definitions
def send(msg, client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def wait_for_server_input(client):
    while True:
        print(client.recv(2048).decode(FORMAT))


#Buttons
class InviteButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        send(f"{clientName},INVITE,aiden", client)

class AcceptButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        pass
        
class RejectButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        #call function
        pass
class InputBox(arcade.gui.UIInputText):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        pass

inputText = ""

#Home view
class Home(arcade.View):
    def __init__(self):
        super().__init__()
        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.csscolor.GRAY)
        self.v_box = arcade.gui.UIBoxLayout()
        invite_button = InviteButton(text="Invite Player", width=400)
        accept_button = AcceptButton(text="Accept Invite", width=400)
        reject_button = RejectButton(text="Reject Invite", width=400)
        input_box = InputBox(text = "Input player name", width = 400)
        self.v_box.add(invite_button)
        self.v_box.add(accept_button)
        self.v_box.add(reject_button)
        self.v_box.add(input_box)
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
        

def main():

    #socket functionality
    client.connect(ADDR) #connect to server
    send(clientName, client) #send client name to server
    thread = threading.Thread(target = wait_for_server_input, args = [client])
    thread.start()

    #Arcade functionality
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = Home()
    window.show_view(game_view)

    arcade.run()

main()
