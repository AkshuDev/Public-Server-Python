import socket
import server_Handler

PORT = 5050

HEADER = 64

DISCONNECT_MESSAGE = "!Disconnect"
KILL_MESSAGE = "!Kill"
DELETE_MESSAGE = "!Delete"
MSGLIST_KM = [DISCONNECT_MESSAGE, KILL_MESSAGE, DELETE_MESSAGE]

FORMAT = "utf-8"

SERVER_NAME = input("Server Name: ")
SERVER_NAME, SERVER = server_Handler.Handler().get_Servers(SERVER_NAME)

if not SERVER:
    print("Server not found")
    exit(1)

ADDR = (SERVER, PORT)

serverMG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverMG.connect(ADDR)

connected = True

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    serverMG.send(send_len)
    serverMG.send(message)
    msg_ = serverMG.recv(2048).decode(FORMAT)
    print(msg_)

while connected:
    msg = input("<@>$: ")
    send(msg)
    if msg in MSGLIST_KM:
        msg = msg + " FSvMa CODE - SMA_1133"
        send(msg)
        exit(1)
    else:
        print(f"[{msg}] is not recognized as an approved Server Management Message.")