import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

#userInput = input("Input Here: ")
message = "heshi,NEW"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #creates socket object
    s.connect((HOST, PORT)) #connect to server
    s.sendall(bytes(message, 'utf-8')) #send message
    data = s.recv(1024) #read server reply

print(f"Received {data!r}")