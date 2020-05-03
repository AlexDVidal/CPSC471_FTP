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
	

########################################################
# Calculates the size of a buffer and attaches
# that size as a string to the head of the
# buffer.
# @param buff - the buffer to be sent
# @param headSize - the size of the header
# @return headBuff - the buffer with header affixed
########################################################
def attachHeader(buff, headSize):
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
	headBuff = dataSizeStr + buff	
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
		numSent += sock.send(data[numSent:].encode())


#########################################################
# Recieves data on the provided socket
# @param socket - the socket to send data on
# @return - the data received, and empty str means eof
#            was found
#########################################################
def recvData(sock, headSize):
	#data buffer	
	data = ""
	# The temporary buffer to store the received
	# data.
	recvBuff = ""
	
	# The size of the incoming file
	recvSize = 0	
	
	# The buffer containing the file size
	recvSizeBuff = ""
	
	# Receive the first 10 bytes indicating the
	# size of the file
	recvSizeBuff = recvAll(sock, headSize)
	if not recvSizeBuff:
		return ""
		
	# Get the file size
	recvSize = int(recvSizeBuff)
	
	# Get the file data
	data = recvAll(sock, recvSize)
	if not data:
		return ""

	return data

