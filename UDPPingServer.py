from socket import *
import time

# What's your IP address and witch port should we use?
receive_host = '127.0.0.1'
receive_port = 30000

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind((receive_host, receive_port))

while True:
  message, address = serverSocket.recvfrom(1024)
  message = message.decode()
  print('Receive: ' + message)

  message = message[0:5] + '1' + message[6:10] + message[10:40] # changing ping to pong
  
  serverSocket.sendto(message.encode(), address)

  time.sleep(1) # wait 1sec before sending the next packet