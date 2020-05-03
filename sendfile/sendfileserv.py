
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
		commandData = ftp_helper.recvData(clientSock, headerSize)
		
		if not commandData:
			print("Client disconnnected.\n")
			
		#debug
		#print(commandData)
		
		tokens = commandData.split(" ")
		#Handle quit command
		if(tokens[0] == "quit"):
			response = "quit ok"
			ftp_helper.sendData(clientSock, response, headerSize)

			# Close socket now that quit has been received
			clientSock.close()
			print("Quit SUCCESSFUL. Closed socket to client.\n");
			break


		# ////////////////////////////
		# Second socket
		elif tokens[0] == "set":
			dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			dataSocket.bind(('', 12000))
			dataSocket.listen(1)
			print("Waiting for second socket connections...")
			clientSock2, addr2 = socket2.accept()
			print("Accepted second connection from client: ", addr2)
			print("\n")
			fileData = ftp_helper.recvData(clientSock2,headerSize)
			if not fileData:
				print("Client disconnected data socket.")
			print(fileData)

		#Handle malformed command		
		else:
			response = "error"
			ftp_helper.sendData(clientSock, response, headerSize)
			print("ERROR. Malformed command from client:");
			print(commandData)



			

	
