
# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys

#add the directory above this script to the system path to import the
#helper functions
sys.path.insert(1,"../")
import ftp_helper


# Command line checks 
if len(sys.argv) < 2:
	print("USAGE python " + sys.argv[0] + " <FILE NAME>")
	exit()
    
headerSize = 10
    
# Server address
serverAddr = "localhost"

# Server port
serverPort = int(sys.argv[1])

# Create a TCP socket
comSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
comSock.connect((serverAddr, serverPort))

# The number of bytes sent
while True:
	userInput = input("ftp>")
	tokens = userInput.split(" ")
	numSent = 0

	#if(userInput[0] == "set"):
	#	fileName = userInput[1]
		# The file data
		#fileData = None
	# Keep sending until all is sent
	#	while True:
	#		
	#		# Read 65536 bytes of data
	#		fileObj = open(fileName, "r")
	#		fileData = fileObj.read(65536)
	#		
	#		# Make sure we did not hit EOF
	#		if fileData:
	#			
	#				
	#			# Get the size of the data read
	#			# and convert it to string
	#			dataSizeStr = str(len(fileData))
	#			
	#			# Prepend 0's to the size string
	#			# until the size is 10 bytes
	#			while len(dataSizeStr) < 10:
	#				dataSizeStr = "0" + dataSizeStr
	#		
	#		
	#			# Prepend the size of the data to the
	#			# file data.
	#			fileData = dataSizeStr + fileData	
	#			
	#			# The number of bytes sent
	#			numSent = 0
	#			
	#
	#			# Send the data!
	#			while len(fileData) > numSent:
	#				numSent += comSock.send(fileData[numSent:])
	#		
	#		# The file has been read. We are done
	#		else:
	#			break
	#
	#
	#	print("Sent ", numSent, " bytes.")
		
	#elif(userInput[0] == "get"):
	#elif(userInput[0] == "ls"):

	commandData = userInput	
	ftp_helper.sendData(comSock, commandData, headerSize)
	if(tokens[0] == "quit"):
		

		response = ftp_helper.recvData(comSock, headerSize)

		if not response:
			print("Server disconnected unexpectedly.")
		
		print("Quitting out.")	
		comSock.close()
		exit()

	elif(tokens[0] == "set"):
		# //////////////////////////////////////
		# 2nd Socket
		print("Set command. Sending message")
		f = open(tokens[1], "r")
		serverPort2 = 12000
		dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		dataSocket.connect((serverAddr, serverPort2))
		message2 = f.read()
		f.close()
		ftp_helper.sendData(dataSocket,message2,headerSize)

	elif(tokens[0] == "get"):
		if len(tokens) != 2:
			print("Malformed command. Usage: get <filename>")
			continue
		commandData = userInput

		ftp_helper.sendData(comSock, commandData, headerSize)
		response = ftp_helper.recvData(comSock, headerSize).split(" ")
		if len(response) == 0:
			print("Server disconnected unexpectedly.")
			break
		elif(response[0] != "get" or len(response) < 4):
			print(" ".join(response))
			continue
		#expect a response of the form "get ok port <num>
		dataPort = int(response[3])
		
		#confirmation received, connect data socket and get data
		dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		dataSocket.connect((serverAddr, dataPort))
		data = ftp_helper.recvData(dataSocket, headerSize)
		try:
			dataFile = open(tokens[1], "w")
		except Exception as exc:
			print("ERROR writing file.", exc)
			continue
		else:
			dataFile.write(data)
			dataFile.close()
			print("got file", tokens[1], len(data), "bytes.\n")

	elif(tokens[0] == "ls"):
		commandData = userInput

		ftp_helper.sendData(comSock, commandData, headerSize)
		response = ftp_helper.recvData(comSock, headerSize).split(" ")
		if len(response) == 0:
			print("Server disconnected unexpectedly.")
			break
		elif(response[0] != "ls" or len(response) < 4):
			print(" ".join(response))
			continue
		#expect a response of the form "ls ok port <num>
		dataPort = int(response[3])
		
		#confirmation received, connect data socket and get data
		dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		dataSocket.connect((serverAddr, dataPort))
		data = ftp_helper.recvData(dataSocket, headerSize)
		print(data)

	else:
		print("Unknown command.")
		continue


		
	
# Close the socket and the file
# fileObj.close()
	


