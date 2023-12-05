from socket import *
import sys
import os
import time
from calendar import day_abbr, month_abbr
from urllib.parse import unquote, urlparse


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
response = ''

while True:
    clientSock, clientAdd = proxSock.accept()

    req = clientSock.recv(1024).decode() #max bytes receiving at once

    req_path = urlparse(req.split()[1]).path
    fname = unquote(req_path).lstrip('/')

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the full path by joining the script directory and the extracted filename
    full_path = os.path.join(script_dir, fname)

    fileName = req.split()[1].strip('/')

    httpMethod = req.split()[0]

    if("%" in full_path): #space or other invalid character. They've all got %
        print(400)
        response = http400.encode()
    elif(httpMethod=="GET"):
        try:

            last_modified_time = os.path.getmtime(full_path)
            last_modified = time.gmtime(last_modified_time)
            last_modified_str = f"{day_abbr[last_modified.tm_wday]}, {last_modified.tm_mday} {month_abbr[last_modified.tm_mon]} {last_modified.tm_year} {last_modified.tm_hour}:{last_modified.tm_min}:{last_modified.tm_sec} GMT"

            # Check if the file was modified in the last n seconds
            current_time = time.time()
            if current_time - last_modified_time < 3:
                print(304) #if the file is not over the ttl get the local version
                clientSock.send(http304.encode())
                response = http304.encode()
                with open(full_path, 'r') as local_file:
                    fdata = local_file.read()
                clientSock.send(fdata.encode())
            else:
                hostSock = socket(AF_INET, SOCK_STREAM, 0)
                hostSock.connect(("127.0.0.1",80)) #connect to the web server
                hostSock.send(f"GET /{fileName} HTTP/1.0".encode())
                clientSock.send(http200.encode())


                with open(full_path, 'w') as cache_file:
                    count=0
                    while(True):
                        res=hostSock.recv(2048).decode()
                        count=count+1
                        if(count!=1):
                            cache_file.write(res)
                        if(len(res)>0):
                            clientSock.send(res.encode())
                        else:
                            break
                    hostSock.close()
                
            
        except IOError: #file not in cache
            hostSock = socket(AF_INET, SOCK_STREAM, 0)
            if(True):
                hostSock.connect(("127.0.0.1",80)) #connect to the web server
                hostSock.send(f"GET /{fileName} HTTP/1.0".encode())
                
                with open(full_path, 'w') as cache_file:
                    count=0
                    while(True):
                        res=hostSock.recv(2048).decode()
                        count=count+1
                        if(count!=1):
                            cache_file.write(res)

                        if(len(res)>0):
                            clientSock.send(res.encode())
                        else:
                            break
                        hostSock.close()
                    clientSock.send(http200.encode())
    clientSock.close()
clientSock, clientAdd = servSock.accept()


proxSock.close()
sys.exit()

#Using only what we know from Module 2 slides 29-34

#The main difference between a proxy server and a web server is that for requests that cannot be met from the locally stored files, a web server
#responds "404 file not found" while when a proxy server is unable to fill a request from a client it acts as a client to a web server to 
#fetch the requested file and then serve it from its cache/local storage.

#the non 404 responses such as 403, 400, 411 etc remain the same along with 200, while 304 serves the cached file and 
#a proxy server will only respond 404 when the origin server it acts as a client to responds 404.

#A minimal proxy server would ensure that the requests are well formed (valid http get request) and check its cache for the requested resource. If it is found and still 
#has time left to live then 304 is returned along with the resource. Otherwise it acts as a client to fetch the requested resource from the origin 
#server and sends it to the origional client once the resource is recieved.

#Decide the test procedure to show it's working. Are client-side
#changes needed? If yes then describe them and find alternative
#ways to test the server-side functionality

#In order to test the proxy server one can enter "http://127.0.0.1:8080/test.html" into the address bar of a web browser. if a web page loads
#then the proxy server worked as the only way for it to fetch a page initially is to fetch the page from the web server. The proxy server 
# can be observed working by using print statements as well

#Bonus- Does your server have an HOL problem? Module 2 slide 36
#If yes, make changes in your server to avoid it 
#and explain what you have done. 
#If no, explain why your server does not have this problem.

#The server is susceptible to HOL blocking this could be fixed by either breaking the packets up into smaller constituent parts and using
# a round robin to send them out roughly at the same time, or by implementing multithreading so each time a request comes in a process on a 
# thread is created to handle it. If this were done the smaller objects could be transmitted concurently with the large one as long as 
# resorces and clock/transmit time are shared  

#HOL- Head of Line. (Big) Packet at the front blocks packets at the back from
#going through, even if they could have been easily processed