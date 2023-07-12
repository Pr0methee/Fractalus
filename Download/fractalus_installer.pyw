import socket,sys,tkinter.messagebox as messagebox,os

HOST = "192.168.56.1"
PORT=50000

mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('trying to connect')
try:
    mySocket.connect((HOST,PORT))
except:
    print('err')
    messagebox.showerror('',"We're not able to join the server, please try again later.")
    sys.exit()
print('connected')
msgServeur = mySocket.recv(1024).decode("Utf8")
tronc = msgServeur.split('µ')

print('Running...',msgServeur)
while 1:
    if msgServeur.upper() == 'END':
        break
    print(msgServeur)
    
    if tronc[0]=='1':
        os.mkdir(tronc[1])
    elif tronc[0]=='2':
        name=tronc[1]
        mySocket.send("OK".encode('Utf8'))
        w = int(mySocket.recv(1024).decode("Utf8"))
        print(w)
        mySocket.send("OK".encode('Utf8'))
        with open(name,"wb") as f:
            f.write(mySocket.recv(w+25))
        print('end')
    
    mySocket.send("OK".encode('Utf8'))
    msgServeur = mySocket.recv(1024).decode("Utf8")
    tronc = msgServeur.split('µ')
