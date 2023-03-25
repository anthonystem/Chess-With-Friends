import socket
import time
import threading
import sys

HEADER = 64 
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" 
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
clientName = sys.argv[1]



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


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setup socket
    client.connect(ADDR) #connect to server
    send(clientName, client) #send client name to server
    inputToSend = input("Input: ")
    send(inputToSend, client)
    thread = threading.Thread(target = wait_for_server_input, args = [client])
    thread.start()
    while True:
        inputToSend = input("Input: ")
        send(inputToSend, client)

main()