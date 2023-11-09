import socket
import threading
import server_Handler
import keyboard
import time

PORT = 5050

HEADER = 64
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!Disconnect"
KILL_MESSAGE = "!Kill"

msg_list = [KILL_MESSAGE]

SERVER = socket.gethostbyname(socket.gethostname())

ServerNAME = input("Server Name: ")
server_CMD_Control = input("Server Control: ")
if 'cmd' in server_CMD_Control.lower():
    server_CMD_Control = True
elif 'manual' in server_CMD_Control.lower():
    server_CMD_Control = False
else:
    print("Server CMD Control set to [FALSE]")
    server_CMD_Control = False

ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def killServer():
    server_Handler.Handler(SERVER).kill_Server(ServerNAME)
    print(f"Killing Server [{SERVER}]")
    server.close()
    print(f"Server [{ServerNAME}] [{SERVER}] is now Stopped")
    exit(1)

def HandleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                print(f"Connection closed from [{addr}]")
                connected = False
            else:
                print(f"[{addr}] {msg}")
                conn.send(f"Message Recived from [{addr}]".encode(FORMAT))
    conn.close()

def start():
    server_Handler.Handler(SERVER).add_Server(ServerNAME)
    print(f"Server Started [{SERVER}] with {server_Handler.Handler(SERVER).get_All_Servers()}")
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=HandleClient, args=(conn, addr))
        thread.daemon = True
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        if server_CMD_Control:
            msg = input(">$:")
            if msg in msg_list:
                if msg == KILL_MESSAGE:
                    conn.send("!Disconnect".encode(FORMAT))
                    time.sleep(5)
                    killServer()
        if keyboard.is_pressed('c'):
            conn.send("!Disconnect".encode(FORMAT))
            time.sleep(5)
            killServer()

print("[STARTING] server is starting...")
start()