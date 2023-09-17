import socket
import threading


IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
nb_clients = 0

clientposes = []
dontadd = 0
index = 0

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
        if str(msg)[0] == "c":
            
            #print(f"[{addr}] {msg}")
            msg = msg.replace("c","")
            dontadd = 0
            index = 0
            for clientpos in clientposes:
                if clientpos[0] == addr[1]:
                    dontadd = 1
                if clientpos[1] != msg:
                    if clientpos[0] == addr[1]:
                        clientposes[index] = (clientposes[index][0],msg)
                    
                index +=1
            if dontadd == 0:
                clientposes.append((addr[1],msg))
        msg = ""
        for clientpos in clientposes:
            print(str(clientpos))
            msg = msg+ str(clientpos) + ","
        conn.send(str(clientposes).encode(FORMAT))

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

    