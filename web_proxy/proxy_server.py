from socket import *
import sys
import os
import time
from calendar import day_abbr, month_abbr


http200 = "HTTP/1.1 200 OK\n" #Done
http304 = "HTTP/1.1 304 Not Modified\n" #Done, needs to be edited to work with remote files and not local
http400 = "HTTP/1.1 400 Bad Request\n" #Done? If HTTP method not valid? Definition:Error not any of the others.
http404 = "HTTP/1.1 404 Not Found\n" #Done
http411 = "HTTP/1.1 411 Length Required\n" #Done
http418 = "HTTP/1.1 418 Im A Teapot\n" #Not Required

proxSock = socket(AF_INET, SOCK_STREAM, 0)
host = "127.0.0.1"
port = 8080
proxSock.bind((host, port))
proxSock.listen(69)

while True:
    clientSock, clientAdd = proxSock.accept()
    print("Accepted client to proxy", clientAdd[0], ",", clientAdd[1])

    req = clientSock.recv(1024).decode() #max bytes receiving at once
    print(f"Prox Request:\n{req}\nEnd Of Request")

    fname = req.split()[1].strip('/')
    print("Prox Requested File: ", fname.strip('/'))

    httpMethod = req.split()[0]
    print("Prox Request Method: ",httpMethod)

    if("%" in fname): #space or other invalid character. They've all got %
        print(400)
        clientSock.send(http400.encode())
    elif(httpMethod=="GET"):
        try:
            f = open(fname, 'r')

            last_modified_time = os.path.getmtime(fname)
            last_modified = time.gmtime(last_modified_time)
            last_modified_str = f"{day_abbr[last_modified.tm_wday]}, {last_modified.tm_mday} {month_abbr[last_modified.tm_mon]} {last_modified.tm_year} {last_modified.tm_hour}:{last_modified.tm_min}:{last_modified.tm_sec} GMT"
            print(f"Last Modified: {last_modified_str}")

            # Check if the file was modified in the last 300 seconds
            current_time = time.time()
            if current_time - last_modified_time < 300:
                print(304) #if the file is not over the ttl get the local version
                clientSock.send(http304.encode())
                fdata = f.read()
                print(fdata)
                for i in range(len(fdata)):
                    clientSock.send(fdata[i].encode())
                clientSock.send("\n".encode())
                clientSock.close()
            else:
                os.utime(fname, (current_time, current_time)) #else go get the remote version
                fdata = f.read()
                clientSock.send(http200.encode())
                print(fdata)
                for i in range(len(fdata)):
                    clientSock.send(fdata[i].encode())
                clientSock.send("\n".encode())
                clientSock.close()
            
        except IOError: #file not in cache
            print(f"{fname} not in cache")
            hostSock = socket(AF_INET, SOCK_STREAM, 0)
            if(True):#try:
                hostSock.connect(("127.0.0.1",80)) #connect to the web server
                print("Connected to web server")
                hostSock.send(f"GET /{fname} HTTP/1.0".encode())
                while(True):
                    res=hostSock.recv(2048).decode()
                    if(len(res)>0):
                        clientSock.send(res.encode())
                        print(f"THE RES:\n{res}")
                        #if("<!DOCTYPE html>" in res):
                        #    print("It be an HTML")
                    else:
                        break
                #serverRes=tempReq.readlines()
                #f = open(fname, 'wb')
                #for i in range(len(serverRes)):
                #    f.write(serverRes[i].encode())
                #    print(f"Line {i}: {serverRes[i]}")
                #    clientSock.send(serverRes[i])
                clientSock.send(http200.encode())
clientSock, clientAdd = servSock.accept()
#print("Accepted client", clientAdd[0], ",", clientAdd[1])



proxSock.close()
sys.exit()

#Using only what we know from Module 2 slides 29-34

#Decide the test procedure to show it's working. Are client-side
#changes needed? If yes then describe them and find alternative
#ways to test the server-side functionality

#Bonus- Does your server have an HOL problem? Module 2 slide 36
#If yes, make changes in your server to avoid it 
#and explain what you have done. 
#If no, explain why your server does not have this problem.

#HOL- Head of Line. (Big) Packet at the front blocks packets at the back from
#going through, even if they could have been easily processed