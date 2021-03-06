##########################################################################
# This file contains functions useful for the client and server to read
# headers, sockets, etc
##########################################################################

import sys
import socket

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes, binary):
	bytesRead = 0
	if binary == True:
		recvBuff = bytes()
	else:
		recvBuff = ""
	# Keep receiving till all is received
	while bytesRead < numBytes:

		if binary == True:
			tmpBuff = sock.recv(numBytes)
		else:
			tmpBuff = sock.recv(numBytes).decode()		

		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
		bytesRead += len(tmpBuff)
	return recvBuff

########################################################
# Calculates the size of a buffer and attaches
# that size as a string to the head of the
# buffer.
# @param buff - the buffer to be sent
# @param headSize - the size of the header
# @return headBuff - the buffer with header affixed
########################################################
def attachHeader(buff, headSize):
	if type(buff) == str:
		buff = bytes(buff.encode())
	# Get the size of the data read
	# and convert it to string
	dataSizeStr = str(len(buff))
	
	#make sure the header is large enough, otherwise return an empty string
	if(len(dataSizeStr) > headSize):
		return ""

	# Prepend 0's to the size string
	# until the size is 10 bytes
	while len(dataSizeStr) < 10:
		dataSizeStr = "0" + dataSizeStr

	# Prepend the size of the data to the
	# file data.
	headBuff = bytes(dataSizeStr.encode()) + buff	
	return headBuff

#########################################################
# Sends data on the provided socket with the correct header
# @param socket - the socket to send data on
# @param data - the data to send on the socket
# @param headSize - the size of the header needed for
#		this package
#########################################################
def sendData(sock, data, headSize):
	data = attachHeader(data, headSize)

	# The number of bytes sent
	numSent = 0

	# Send the data!
	while len(data) > numSent:
		numSent += sock.send(data[numSent:])


#########################################################
# Recieves data on the provided socket
# @param socket - the socket to send data on
# @return - the data received, and empty str means eof
#            was found
#########################################################
def recvDisambig(sock, headSize, binary):
	# Receive the first headSize bytes indicating the
	# size of the file
	recvSizeBuff = recvAll(sock, headSize, False)
	if not recvSizeBuff:
		return ""
		
	# Get the file size
	recvSize = int(recvSizeBuff)
	
	# Get the file data
	data = recvAll(sock, recvSize, binary)
	if not data:
		return ""

	return data

def recvData(sock, headSize):
	return recvDisambig(sock, headSize, binary=False)

def recvDataBinary(sock, headSize):
	return recvDisambig(sock, headSize, binary=True)

