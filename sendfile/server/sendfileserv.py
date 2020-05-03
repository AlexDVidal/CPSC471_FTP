
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************
import sys
import socket
import subprocess

#add the directory above this script to the system path to import the
#helper functions
sys.path.insert(1,"../")
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
	
	print("Accepted connection from client: ", addr, "\n")
	
	#maintain comms with this client until quit received
	while True:
		# The buffer to all data received from the
		# the client.
		commandData = ftp_helper.recvData(clientSock, headerSize)
		
		if not commandData:
			print("Client disconnnected.\n")
			break
			
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
			clientSock2.close()
			dataSocket.close()
		
		elif tokens[0] == "get":
			print("get received")
			
			if(len(tokens) != 2):
				print("get FAILURE. Malformed request.", tokens)
				ftp_helper.sendData(clientSock, "error malformed request", headerSize)
				continue
			try:
				dataFile = open(tokens[1], "r")
				data = dataFile.read(65536)
			except Exception as exc:
				print("get FAILURE.", exc)
				ftp_helper.sendData(
					clientSock, "error in subprocess for get", headerSize)
				continue

			#we have the result of the call to get, make an ephemeral port
			#tell the client the details and send the data
			listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			listenSocket.bind(('', 0))
			listenSocket.listen(1)
			dataPort = listenSocket.getsockname()[1]
			#tell the client what port to connect to
			response = "get ok port " +str(dataPort)
			ftp_helper.sendData(clientSock, response, headerSize)
			
			#block until connection received then send data
			dataSocket, addr = listenSocket.accept()
			print("accepted data connection")
			ftp_helper.sendData(dataSocket, data, headerSize)
			#close the ephemeral sockets
			dataSocket.close()
			listenSocket.close()
			print("get SUCCESS\n")

		elif tokens[0] == "ls":
			print("ls received")
			
			try:
				data = subprocess.check_output(
					tokens, stderr=subprocess.STDOUT).decode()
			except Exception as exc:
				print("ls FAILURE.", exc)
				ftp_helper.sendData(
					clientSock, "error in subprocess for ls", headerSize)
				continue

			#we have the result of the call to ls, make an ephemeral port
			#tell the client the details and send the data
			listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			listenSocket.bind(('', 0))
			listenSocket.listen(1)
			dataPort = listenSocket.getsockname()[1]
			#tell the client what port to connect to
			response = "ls ok port " +str(dataPort)
			ftp_helper.sendData(clientSock, response, headerSize)
			
			#block until connection received then send data
			dataSocket, addr = listenSocket.accept()
			print("accepted data connection")
			ftp_helper.sendData(dataSocket, data, headerSize)
			#close the ephemeral sockets
			dataSocket.close()
			listenSocket.close()
			print("ls SUCCESS\n")
			
		#Handle malformed command		
		else:
			response = "error"
			ftp_helper.sendData(clientSock, response, headerSize)
			print("ERROR. Malformed command from client:");
			print(commandData)

