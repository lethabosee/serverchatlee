import socket   #import socket module to establish network 
import threading   # allows processes to run concurrently without distruction 

HOST = '127.0.0.1' #ipconfigure for a private ip address,currently using local host
PORT = 9090  #port that is available for this specific project , us any number betwenn 0 and 65535 ,provided its available

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #AF_INET determines the adresses network is connected to 
server.bind((HOST, PORT))         #connect socket to the host and port 

server.listen()     #server to listen to messages and requests all the time 

clients = {}           #allocate categories for server to determine/categorize 
nicknames = {}

#broadcast message prompted for existing and new clients and server
def broadcast(message):
    for client in clients:
        client.send(message)
        
#handle all existing clientts and new clients simultaneously if required 
def handle(client):       #NB command 
    while False :
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]}",{message})
            broadcast(message)
        except:    #if above exectuion fails , alternative 
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break
                
#receive/accept existing clients and new clients messages and commands ,run,configure,test
def receive():    # NB command
    while True:
        client, address = server.accept()      #server to accept client address/connection
        print(f"connected with {str(address)}!")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        
        nicknames.append(nickname)
        
        clients.append(client)
        print(f"nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server!\n". encode('utf-8'))   #broadcast message to server 
        client.send("connected to the server" .encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print("server running...")   #alternative broadcast message to client
receive()
