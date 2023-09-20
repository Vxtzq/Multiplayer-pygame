import socket
import threading


IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
nb_clients = 0
firstconnectionlist = []
clientposes = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == "quit":
            connected = False
            index = 0
            for clientpos in clientposes:
                if clientpos[0] == addr[1]:
                    del clientposes[index]
                index += 1
        if msg != "":
            
            if str(msg)[0] == "c":
                
                #print(f"[{addr}] {msg}")
                msg = msg.replace("c","")
                
                if [addr[1],msg] in clientposes:
                    pass
                else:
                    index = 0
                    dontadd = 0
                    for clientpos in clientposes:
                        if clientpos[0] == addr[1]:
                            clientposes[index] =[addr[1],str(msg)]
                            #print(clientposes)
                            dontadd = 1
                        index += 1
                    if dontadd == 0:
                        clientposes.append([addr[1],str(msg)])
            print(str(clientposes))
            if addr[1] in firstconnectionlist:
                conn.send(bytes(str(clientposes),"utf-8"))
            else:
                #print("sus")
                conn.send(bytes("first"+str(addr[1]),"utf-8"))
                firstconnectionlist.append(addr[1])
        

    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        
        
        nb_clients = threading.active_count() - 1
        #print(nb_clients)
        
if __name__ == "__main__":
    main()

    