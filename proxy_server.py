from socket import *
import sys


servSock = socket(AF_INET, SOCK_STREAM, 0)

while True:
    break

servSock.close()
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