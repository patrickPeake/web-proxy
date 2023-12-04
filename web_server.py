from socket import *
import sys
import os
import time
from calendar import day_abbr, month_abbr
#import requests

http200 = "HTTP/1.1 200 OK\n" #Done
http304 = "HTTP/1.1 304 Not Modified\n" #Last-Modified gotten, not added to req/res yet
http400 = "HTTP/1.1 400 Bad Request\n" #Done? If HTTP method not valid? Definition:Error not any of the others.
http403 = "HTTP/1.1 403 Forbidden\n" #Done? Assume it's for non-GET requests?
http404 = "HTTP/1.1 404 Not Found\n" #Done
http411 = "HTTP/1.1 411 Length Required\n" #Done
http418 = "HTTP/1.1 418 Im A Teapot\n" #Not Required



servSock = socket(AF_INET, SOCK_STREAM)
host = "127.0.0.1"
port = 80
servSock.bind((host, port))
servSock.listen(69) #size of queue. 0 for only 1 interacting client, 1 for ____?. Can leave blank to set to the default
allow411 = False #because the test.html file doesnt have a contetn length header if we always check for 411 the server will never work. 
# To verify that the 411 response is correct change this to true and it will check/return 411 responses

while True:
    clientSock, clientAdd = servSock.accept()
    print("Accepted client", clientAdd[0], ",", clientAdd[1])

    req = clientSock.recv(1024).decode() #max bytes receiving at once
    print(f"Request:\n{req}\nEnd Of Request")


    headers = req.split('\r\n\r\n', 1)[0]  # Extract headers from the request

    # Check if Content-Length header is present
    if allow411:
        if 'Content-Length' in headers:
            content_length = int(headers.split('Content-Length: ')[1].split('\r\n')[0])
            print(f"Content-Length: {content_length}")
        else:
            print("Content-Length header not found")
            print(411)
            clientSock.send(http411.encode()) #returns 411 if the content-length header is not included
            break

    fname = req.split()[1].strip('/')
    print("Requested File: ", fname.strip('/'))

    httpMethod = req.split()[0]
    print("Request Method: ",httpMethod)

    if("%" in fname): #space or other invalid character
        print(400)
        clientSock.send(http400.encode())
    
    if(httpMethod in ["POST", "PUT", "DELETE", "PATCH"]):
        print(403)
        clientSock.send(http403.encode())
    elif(httpMethod=="GET"):
        try:
            f = open(fname, 'r')

            #lastModified = time.gmtime(os.path.getmtime(fname))
            #lastModifiedString=f"{day_abbr[lastModified.tm_wday]}, {lastModified.tm_mday} {month_abbr[lastModified.tm_mon]} {lastModified.tm_year} {lastModified.tm_hour}:{lastModified.tm_min}:{lastModified.tm_sec} GMT"
            #print(f"Last Modified: {lastModifiedString}")

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
