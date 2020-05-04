# CPSC471_FTP
Assignment 1, File Transfer Protocol

Project members -
Steven Steele steeletet@csu.fullerton.edu
Alex Vidal avidal@csu.fullerton.edu

Programming language -
Python3

Repository -
https://github.com/AlexDVidal/CPSC471_FTP

How to run the program -
Once extracted the project structure should look like this
<pre>
CPSC471_FTP/
|____ftp_helpers.py
|____server/
|  |____pythonserv.py
|  |____serverFile.txt
|____client/
|  |____pythoncli.py
|  |____clientFile.txt
</pre>
 
Run an instance of the server by calling
    python3 pythonserv.py <port>
where <port> is any number from 1024 to 49151

Run an instance of the client by calling
    python3 pythoncli.py <server> <port>
where <server> is the name of the server to connect to, and 
<port> is the same number as used in the server.
If running the server and the client on the same machine
you can use "localhost" for the server name.
 
On the client side the commands you can enter are
   ls <options>
   set <filename>
   get <filename>
   quit

ls hanldes most options available in the shell, but can't handle regexp.
set and get can both transmit text files and binary files.
