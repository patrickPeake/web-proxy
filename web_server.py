from socket import *
import sys
import os
import time
from calendar import day_abbr, month_abbr

http200 = "HTTP/1.1 200 OK\n" #Done
http304 = "HTTP/1.1 304 Not Modified\n" #Last-Modified gotten, not added to req/res yet
http400 = "HTTP/1.1 400 Bad Request\n" #Done? If HTTP method not valid? Definition:Error not any of the others.
http403 = "HTTP/1.1 403 Forbidden\n" #Done
http404 = "HTTP/1.1 404 Not Found\n" #Done
http411 = "HTTP/1.1 411 Length Required\n" #
http418 = "HTTP/1.1 418 Im A Teapot\n" #



servSock = socket(AF_INET, SOCK_STREAM)
host = "127.0.0.1"
port = 80
servSock.bind((host, port))
servSock.listen(69) #size of queue. 0 for only 1 interacting client, 1 for ____?. Can leave blank to set to the default

while True:
    clientSock, clientAdd = servSock.accept()
    print("Accepted client", clientAdd[0], ",", clientAdd[1])

    req = clientSock.recv(1024).decode() #max bytes receiving at once
    print(f"Request:\n{req}\nEnd Of Request")

    fname = req.split()[1].strip('/')
    print("Requested File: ", fname.strip('/'))

    httpMethod = req.split()[0]
    print("Request Method: ",httpMethod)

    if("%" in fname): #space or other invalid character. They've all got %
        print(400)
        clientSock.send(http400.encode())
    elif(fname.split('/')[0]=="forbidden"): #trying to access forbidden directory
        print(403)
        print("Trying to access /forbidden")
        clientSock.send(http403.encode())
    elif(httpMethod in ["POST", "PUT", "DELETE", "PATCH"]): #trying to use forbidden methods
        print(403)
        clientSock.send(http403.encode())
    elif(httpMethod=="GET"):
        try:
            f = open(fname, 'r')

            lastModified = time.gmtime(os.path.getmtime(fname))
            lastModified=f"{day_abbr[lastModified.tm_wday]}, {lastModified.tm_mday} {month_abbr[lastModified.tm_mon]} {lastModified.tm_year} {lastModified.tm_hour}:{lastModified.tm_min}:{lastModified.tm_sec} GMT"
            print(f"Last Modified: {lastModified}")
            
            fdata = f.read()
            clientSock.send(http200.encode())
            print(fdata)
            for i in range(len(fdata)):
                clientSock.send(fdata[i].encode())
            clientSock.send("\n".encode())
            clientSock.close()

        except IOError: #file not in directory
            print(404)
            clientSock.send(http404.encode())
    else: #http method wasn't valid
        print(400)
        clientSock.send(http400.encode())
    break

servSock.close()
sys.exit()
#Test using test.html and copy results. Can edit messages
#http://127.0.0.1/test.html gets file
