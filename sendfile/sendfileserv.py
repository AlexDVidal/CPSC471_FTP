
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************
import sys
import socket

# Command line checks 
if len(sys.argv) < 2:
	print("USAGE python " + sys.argv[0] + " <FILE NAME>")
	exit()

# The port on which to listen
listenPort = int(sys.argv[1])

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', listenPort))

# Start listening on the socket
welcomeSock.listen(1)

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes).decode()
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff
		
# Accept connections forever
while True:
	
	print("Waiting for connections...")
		
	# Accept connections
	clientSock, addr = welcomeSock.accept()
	
	print("Accepted connection from client: ", addr)
	print("\n")
	
	#maintain comms with this client until quit received
	while True:
		# The buffer to all data received from the
		# the client.
		command = ""
		
		# The temporary buffer to store the received
		# data.
		recvBuff = ""
		
		# The size of the incoming file
		commandSize = 0	
		
		# The buffer containing the file size
		commandSizeBuff = ""
		
		# Receive the first 10 bytes indicating the
		# size of the file
		commandSizeBuff = recvAll(clientSock, 10)
		if not commandSizeBuff:
			break
			
		print("Size of buffer is ", commandSizeBuff)
		# Get the file size
		commandSize = int(commandSizeBuff)
		
		print("The command size is ", commandSize)
		
		# Get the file data
		commandData = recvAll(clientSock, commandSize)
		if not commandData:
			break		

		print("The command is: ")
		print(commandData)
			
		# Close our side if quit is received
		#clientSock.close()
	
