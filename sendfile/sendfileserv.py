
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************
import sys
import socket
import ftp_helper

# Command line checks 
if len(sys.argv) < 2:
	print("USAGE python " + sys.argv[0] + " <FILE NAME>")
	exit()

headerSize = 10

# The port on which to listen
listenPort = int(sys.argv[1])

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', listenPort))

# Start listening on the socket
welcomeSock.listen(1)
		
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
		commandSizeBuff = ftp_helper.recvAll(clientSock, 10)
		if not commandSizeBuff:
			print("Client disconnected.\n")
			break
			
		# Get the file size
		commandSize = int(commandSizeBuff)
		
		
		# Get the file data
		commandData = ftp_helper.recvAll(clientSock, commandSize)
		if not commandData:
			print("Client disconnected.\n")
			break		

		#we have a command, time to parse it
		print(commandData)
		
		#for testing, send the command as a response
		response = commandData
		response = ftp_helper.attachHeader(response, headerSize)
		numSent = 0
		while len(response) > numSent:
			numSent += clientSock.send(response[numSent:].encode())
			print("sent", numSent, "bytes")


		print("Sent ", numSent, " bytes in total.")


		commandData = commandData.split()
		
			
		# Close our side if quit is received
		#clientSock.close()
	
