# CPSC471_FTP
Assignment 1, File Transfer Protocol

Project members -
Steven Steele steeletet@csu.fullerton.edu
Alex Vidal avidal@csu.fullerton.edu

Programming language -
Python3

How to run the program -
Once extracted the project structure should look like this

CPSC471_FTP/  
|____ftp_helpers.py  
|____server/  
\|\  \|____sendfileserv.py  
|  |____serverFile.txt  
|____client/  
|  |____sendfilerscli.py  
|  |____clientFile.txt  
 
Run an instance of the server by calling
    python3 sendfileserv.py <port>
where <port> is any number from 1024 to 49151

Run an instance of the client by calling
    python3 sendfilescli.py <port>
where <port> is the same number as used in the server.
By default the client uses localhost as the ip address for the server,
so this project is designed to be run on one device.

On the client side the commands you can enter are
   ls <options>
   set <filename>
   get <filename>
   quit
