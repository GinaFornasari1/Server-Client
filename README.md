# Server-Client
A basic python based Server-Client application for file transfers.

Description: 
Creating a socket, binding it to a specific address and port, and send/download files over a Peer-to-Peer network. A Server-Client model is used with TCP sockets. A client can upload, download, or list the files in the ServerFiles folder. A user can encrypt a file with a symmetric key upon upload. 

Usage Directions:
This application is run through the terminal. The Server runs on the first terminal, where it displays it's IP address, the number of connected devices and feedback on client activities. On a new terminal, the client file is run using the command: finalClient.py [SERVER_IP] [SERVER_PORT] [COMMAND] .
The [COMMAND] can be "upload", "download", or "list". Coupled with this, a user can encrypt a file upon upload but this will mean that the client must decrypt this file on an attempted download using a symmetric key. The user follows directions from here onward (note, the suffix is included on file name inputs).
The files are stored in the "ServerFiles" folder with an automatic prefix added. Upon download, the files are added to "Client_Files". 
The port is set to 5050.
