import socket
from clientgui import *
import ast

globalid = 0
IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
entities = []
ids = []
idsreceived = []
def main():
    global ids, idsreceived
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
    
    connected = True
    while connected:
        xtosend, ytosend, msgtosend = run()
        msg = 'c' + str([xtosend,ytosend])
        screen.fill((0, 0, 0))
        
        if msgtosend == "":
            client.send(msg.encode(FORMAT))
        else:
            client.send("quit".encode(FORMAT))
        

        if msg == DISCONNECT_MSG:
            connected = False
        else:
            msg = client.recv(SIZE).decode(FORMAT)
            if msg[0] != "f":
                res = ast.literal_eval(msg)
                
                counter = 0
                ids = []
                idsreceived = []
                for clientpos, entity in zip(res, entities):
                    ids.append(entity.ID)
                    idsreceived.append(int(clientpos[0]))
                for idclient in ids:
                    if idclient in idsreceived:
                        pass
                    else:
                        print("kill")
                        index = 0
                        for clientobj in entities:
                            if clientobj.ID == idclient:
                                del entities[index]
                            index += 1
                            
                for clientpos in res:
                    pos = clientpos
                    clientid = pos[0]
                    clientxy = ast.literal_eval(pos[1])
                    
                    index = 0
                    dontadd = 0
                    for entity in entities:
                        if entity.ID == clientid:
                            entity.x = clientxy[0]
                            entity.y = clientxy[1]
                            index += 1
                            dontadd = 1
                    
                    if dontadd == 0:
                        if clientid != globalid:
                            entity = Entity(clientxy[0],clientxy[1],clientid)
                            entities.append(entity)
            else:
                globalid = int(msg.replace("first",""))
                print("global" +str(globalid))
        
        for entity in entities:
            #print("test")
            entity.update()
        player.update()
                
            
            #print(res[0])
            
            #print(f"[SERVER] {msgtosend}")
        
            

if __name__ == "__main__":
    main()
