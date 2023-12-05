from socket import *
import sys
import os
import time
from calendar import day_abbr, month_abbr


http200 = "HTTP/1.1 200 OK\n" #Done
http304 = "HTTP/1.1 304 Not Modified\n" #Done, needs to be edited to work with remote files and not local
http400 = "HTTP/1.1 400 Bad Request\n" #Done? If HTTP method not valid? Definition:Error not any of the others.
http403 = "HTTP/1.1 403 Forbidden\n" #Done
http404 = "HTTP/1.1 404 Not Found\n" #Done
http411 = "HTTP/1.1 411 Length Required\n" #Done
http418 = "HTTP/1.1 418 Im A Teapot\n"



servSock = socket(AF_INET, SOCK_STREAM)
host = "127.0.0.1"
port = 80
servSock.bind((host, port))
servSock.listen(69) #size of queue. 0 for only 1 interacting client, 1 for ____?. Can leave blank to set to the default
allow411 = False #test.html doesnt have a content length header, so checking for it will always result in 411 
#To allow 411 response set allow411=True

while True:
    response = ''
    clientSock, clientAdd = servSock.accept()
    #print("Accepted client", clientAdd[0], ",", clientAdd[1])

    req = clientSock.recv(1024).decode() #max bytes receiving at once
    #print(f"Request:\n{req}\nEnd Of Request")


    headers = req.split('\r\n\r\n', 1)[0]  # Extract headers from the request

    # Check if Content-Length header is present
    if allow411:
        if 'Content-Length' in headers:
            content_length = int(headers.split('Content-Length: ')[1].split('\r\n')[0])
            #print(f"Content-Length: {content_length}")
        else:
            #print("Content-Length header not found")
            print(411)
            response = http411.encode() #returns 411 if the content-length header is not included
            break

    fname = req.split()[1].strip('/')
    #print("Requested File: ", fname.strip('/'))

    httpMethod = req.split()[0]
    #print("Request Method: ",httpMethod)

    if("%" in fname): #space or other invalid character. They've all got %
        print(400)
        response = http400.encode()
    elif(fname.split('/')[0]=="forbidden"): #trying to access forbidden directory
        print(403)
        #print("Trying to access /forbidden")
        response = http403.encode()
    elif(httpMethod in ["POST", "PUT", "DELETE", "PATCH"]): #trying to use forbidden methods
        print(403)
        response = http403.encode()
    elif(httpMethod=="GET"):
        try:
            f = open(fname, 'r')

            last_modified_time = os.path.getmtime(fname)
            last_modified = time.gmtime(last_modified_time)
            last_modified_str = f"{day_abbr[last_modified.tm_wday]}, {last_modified.tm_mday} {month_abbr[last_modified.tm_mon]} {last_modified.tm_year} {last_modified.tm_hour}:{last_modified.tm_min}:{last_modified.tm_sec} GMT"
            #print(f"Last Modified: {last_modified_str}")

            # Check if the file was modified in the last 300 seconds
            current_time = time.time()
            if current_time - last_modified_time < 300:
                print(304) #if the file is not over the ttl get the local version
                clientSock.send(http304.encode())
                response = http304.encode()
                fdata = f.read()
                clientSock.send(fdata.encode())
            else:
                os.utime(fname, (current_time, current_time)) #else go get the remote version
                print(200)
                fdata = f.read()
                clientSock.send(http200.encode())
                response = http200.encode()
                clientSock.send(fdata.encode())
        except IOError: #file not in directory
            if(response == ''):
                #print("in 404")
                print(404)
                response = http404.encode()
    else: #http method wasn't valid
        print(400)
        response = http400.encode()
    if(response != http304.encode() and response != http200.encode() and response != ''):
        clientSock.send(response)
    clientSock.close()
    #break

servSock.close()
sys.exit()
#Test using test.html and copy results. Can edit messages
#http://127.0.0.1/test.html gets file
