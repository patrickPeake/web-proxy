from socket import * # to test the web server responses please run "python.py" in this directory
import sys             #the expected output is 200 403 403 404
import os
import time
from calendar import day_abbr, month_abbr
from urllib.parse import unquote, urlparse


http200 = "HTTP/1.1 200 OK\n" #Done
http304 = "HTTP/1.1 304 Not Modified\n" #Done, needs to be edited to work with remote files and not local
http400 = "HTTP/1.1 400 Bad Request\n" #Done? If HTTP method not valid? Definition:Error not any of the others.
http403 = "HTTP/1.1 403 Forbidden\n" #Done
http404 = "HTTP/1.1 404 Not Found\n" #Done
http411 = "HTTP/1.1 411 Length Required\n" #Done to test is please set "allow411" to true
http418 = "HTTP/1.1 418 Im A Teapot\n" #Not Required



servSock = socket(AF_INET, SOCK_STREAM)
host = "127.0.0.1"
port = 80
servSock.bind((host, port))
servSock.listen(69) #size of queue. 0 for only 1 interacting client, 1 for ____?. Can leave blank to set to the default
allow411 = False #trying to fetch test.html doesnt have a content length header, so checking for it will always result in 411 
#To allow 411 response set allow411=True

while True:
    response = ''
    clientSock, clientAdd = servSock.accept()

    req = clientSock.recv(1024).decode() #max bytes receiving at once


    headers = req.split('\r\n\r\n', 1)[0]  # Extract headers from the request

    # Check if Content-Length header is present
    if allow411:
        if 'Content-Length' in headers:
            content_length = int(headers.split('Content-Length: ')[1].split('\r\n')[0])
        else:
            print(411)
            response = http411.encode() #returns 411 if the content-length header is not included
            clientSock.send(response)
            clientSock.close()
            continue

    req_path = urlparse(req.split()[1]).path
    fname = unquote(req_path).lstrip('/')

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the full path by joining the script directory and the extracted filename
    full_path = os.path.join(script_dir, fname)


    httpMethod = req.split()[0]

    if("%" in full_path): #space or other invalid character. They've all got %
        print(400)
        response = http400.encode()
    elif(fname.split('/')[0]=="forbidden"): #trying to access forbidden directory
        print(403)
        response = http403.encode()
    elif(httpMethod in ["POST", "PUT", "DELETE", "PATCH"]): #trying to use forbidden methods
        print(403)
        response = http403.encode()
    elif(httpMethod=="GET"):
        try:
            f = open(full_path, 'r')
            last_modified_time = os.path.getmtime(full_path)
            last_modified = time.gmtime(last_modified_time)
            last_modified_str = f"{day_abbr[last_modified.tm_wday]}, {last_modified.tm_mday} {month_abbr[last_modified.tm_mon]} {last_modified.tm_year} {last_modified.tm_hour}:{last_modified.tm_min}:{last_modified.tm_sec} GMT"
            
            # Check if the file was modified in the last 300 seconds
            current_time = time.time()
            if current_time - last_modified_time < 3:
                print(304) #if the file is not over the ttl get the local version
                clientSock.send(http304.encode())
                response = http304.encode()
                fdata = f.read()
                clientSock.send(fdata.encode())
            else:
                os.utime(full_path, (current_time, current_time)) #else go get the remote version
                print(200)
                fdata = f.read()
                clientSock.send(http200.encode())
                response = http200.encode()
                clientSock.send(fdata.encode())
        except IOError: #file not in directory
            if(response == ''):
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