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
