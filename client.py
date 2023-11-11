import socket
from server_Handler import Handler

PORT = 5050

HEADER = 64
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!Disconnect"

name = input("Enter Server Name: ")

name, SERVER = Handler().get_Servers(name)

if not SERVER:
    print("Server not found")
    exit(1)

ADDR = (SERVER, PORT)
print(ADDR)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

connected = True

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)
    msg_ = client.recv(2048).decode(FORMAT)
    if msg_ == DISCONNECT_MESSAGE:
        connected = False
        print('Connection Closed')
        client.close()
        exit(1)
    print(msg_)

while connected:
    try:
        msg = input(">$: ")
        send(msg)
        if msg == DISCONNECT_MESSAGE:
            connected = False
    except Exception:
        print(f"Server [{name}] is disconnected")
        exit(1)