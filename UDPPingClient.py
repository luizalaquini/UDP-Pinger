# T2 - Redes
# Luiza Batista Laquini
# 2019107786

# Importing necessary libraries
from socket import *
from statistics import stdev
import time

# IP address and port number to socket
remote_host = '168.227.188.22'
remote_port = 30000

# Defining some needed variables and constants 
message = "luiza"
number_of_pings = 10
packages_sent = 0
packages_received = 0
rtts = []
total_time = 0

# Create a UDP socket for the client
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(2)

# =========================== Functions ===========================

def format_message(message):
  '''
  This function formats the message as defined by the professor.
  There is a 40 bytes sequence of:
  - 5 bytes for the sequence number
  - 1 byte for the type of message (0 for ping or 1 for pong)
  - 4 bytes for the timestamp 
  - 30 bytes for the message itself
  '''
  sequence_number = str(i).rjust(5,'0')
  timestamp = str(int(rtt / 1000000) % 10000).rjust(4,'0') 
  autocomplete = str(message).ljust(30,'\0') 

  full_message = sequence_number + '0' + timestamp + autocomplete 

  return full_message

def handle_message(message_sent, message_received)-> bool:
  '''
  This function handles the message received from the server.
  It checks if the message received is the same as the one sent and returns true or false.
  '''
  # Parsing the message sent
  seq_num_s = message_sent[0:5]
  type_s = message_sent[5:6]
  ts_s = message_sent[6:10]
  msg_s = message_sent[10:40]
  # Parsing the message received
  seq_num_r = message_received[0:5]
  type_r = message_received[5:6]
  ts_r = message_received[6:10]
  msg_r = message_received[10:40]

  # Comparing the messages
  if len(message_received) != 40:
    return False
  elif type_r != '1':
    return False
  elif seq_num_s != seq_num_r:
    return False
  elif msg_s != msg_r:
    return False
  elif ts_s != ts_r:
    return False
  return True

# =========================== Main ===========================

for i in range(0, number_of_pings):  
  # Start the rtt timer (in nanoseconds)
  rtt = time.time_ns()
  # Start the total_time counter
  if i == 0: 
    total_time = time.time_ns() 
  
  # Format the message
  full_message = format_message(message)
  # Send the message to the server
  clientSocket.sendto(full_message.encode(), (remote_host, remote_port))
  # Increment the number of packages sent
  packages_sent += 1

  # Try to receive the message from the server
  try:
    # Receiving the message 
    reply = clientSocket.recv(1024)
    message_received = reply.decode()
    seq_num_r = message_received[0:5] # sequence number from the server
    seq_num_s = full_message[0:5] # sequence number from the client

    '''
    Verifying if the sequence number of the package received is the same as the one sent.
    As long as the packet received is not what the client sent, it keeps receiving packets. 
    When the packet received is what the client sent, it exits the while.
    '''
    while int(seq_num_r) < int(seq_num_s): 
      reply = clientSocket.recv(1024)
      message_received = reply.decode()
      seq_num_r = message_received[0:5]  

    # Stop the rtt timer and convert it to milliseconds
    rtt = time.time_ns() - rtt
    rtt = rtt / 1000000 

    # If the message received is the same as the one sent, increment the number of packages received
    if(handle_message(full_message, message_received) is False):
      print('Invalid Package')
    else: 
      rtts.append(rtt)
      print(message_received)
      packages_received += 1

  except:
    print('Package loss [time limit exceeded]')

# Stop the total_time counter and convert it to milliseconds
total_time = time.time_ns() - total_time
total_time = total_time / 1000000

# Calculating the statistics
if packages_received == 0:
  print('Any package received')
else:
  packet_loss = (packages_sent - packages_received) / packages_sent * 100
  rtt_min = min(rtts)
  rtt_max = max(rtts)
  rtt_avg = sum(rtts) / len(rtts)
  rtt_std = stdev(rtts)
  print('{} packages transmitted, {} received, {}% packet loss, time {:.2f}ms rtt min/avg/max/mdev = {:.4f}/{:.4f}/{:.4f}/{:.4f} ms' .format(packages_sent, packages_received, packet_loss, total_time, rtt_min, rtt_avg, rtt_max, rtt_std))