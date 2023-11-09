import pickle
import os

global Servers
Servers = {}

class Handler:
    def __init__(self, server_addr=""):
        self.server_addr = server_addr

    def add_Server(self, name) -> None:
        Servers[name] = self.server_addr
        if os.path.exists(os.getcwd()+"\\Firewall\\ServerHandler_"):
            if not os.path.exists(os.getcwd()+"\\Firewall\\ServerHandler_\\Servers.pkl"):
                with open(os.getcwd()+"\\Firewall\\ServerHandler_\\Servers.pkl", "wb") as ServerPKL:
                    pickle.dump(Servers, ServerPKL)
            else:
                with open(os.getcwd()+"\\Firewall\\ServerHandler_\\Servers.pkl", "rb+") as ServerPKL:
                    ServerData = pickle.load(ServerPKL)
                    if name in ServerData:
                        print(f"Server [{name}] [{self.server_addr}] is rebooted.")
                        return None
                    ServersPkl = {**ServerData, **Servers}
                    ServerPKL.seek(0)
                    pickle.dump(ServersPkl, ServerPKL)
                    
        else:
            os.mkdir(os.getcwd()+"\\Firewall\\ServerHandler_")
            with open(os.getcwd()+"\\Firewall\\ServerHandler_\\Servers.pkl", "wb") as ServerPKL:
                pickle.dump(Servers, ServerPKL)
        print(f"Server [{name}] added from [{self.server_addr}]")

    def kill_Server(self, name) -> None:
        if os.path.exists(os.getcwd()+"\\Firewall\\ServerHandler_\\Servers.pkl"):
            with open(os.getcwd()+"\\Firewall\\ServerHandler_\\Servers.pkl", "rb+") as ServerPKL:
                ServerData = pickle.load(ServerPKL)
                if name in ServerData:
                    del ServerData[name]
                    ServerPKL.seek(0)
                    pickle.dump(ServerData, ServerPKL)
                    print(f"Server [{name}] [{self.server_addr}] is killed.")
                else:
                    print(f"Server [{name}] [{self.server_addr}] is not found.")
        else:
            print(f"Server [{name}] [{self.server_addr}] is not found.")
    
    def get_Servers(self, name):
        if os.path.exists(os.getcwd()+"\\Firewall\\ServerHandler_\\Servers.pkl"):
            with open(os.getcwd()+"\\Firewall\\ServerHandler_\\Servers.pkl", "rb") as ServerPKL:
                ServerData = pickle.load(ServerPKL)
                Servers = ServerData
        else:
            return None, None
        for i in Servers.keys():
            if i == name:
                return Servers[name], Servers.get(name)
        return None, None
    
    def get_All_Servers(self):
        return Servers