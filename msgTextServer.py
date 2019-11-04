#Serve as a server to recieve 8583 text
from socket import *
#from textSolvement import *
import os
import time
from threading import Thread

def msgServer(location):

    server = socket(AF_INET,SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    server.bind((location, 63344))
    server.listen(1)
    conn, addr = server.accept()
    print('Listening....')
    count = 0

    while True:
        data = conn.recv(1024)
        count = count + 1
        conn.send(b'msg recieved')
        print (count , ' ' , data)
            #return data
    #server.close()


if __name__ == '__main__':
    msgServer(location)
    #msgUnpackAndSave()
    #dataRecv = msgServer('外网')

