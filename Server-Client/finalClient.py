import hashlib
import socket 
import os
#import tqdm
import sys

#getting required information from the command line
SERVER= sys.argv[1]
PORT = int(sys.argv[2])
userAct = sys.argv[3]

#defining constants

HEADER = 64
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes at a time

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #STREAM indicates TCP socket

#connecting the client with the server
def connect():
    connection.connect(ADDRESS)

#method that returns a list of all existing file names on the server
def listFiles():
    #recieving the list as a string from the server
    files = connection.recv(BUFFER_SIZE).decode("utf-8")
    print("The files currently stored on the server:\n")
    print(files)
    return

#method called when a user wants to upload a file to the server
def uploadFile():
    file = input("Enter the name of the file to upload:")
    fileSize = os.path.getsize(file)

    with (open(file,'rb')) as fileToSend:
        data = fileToSend.read()
    
    #creating a hash value used later to ensure complete transmission of file
    hashing = hashlib.sha256(data).hexdigest()

    #sending the server the file details
    connection.send(f"{file}{SEPARATOR}{fileSize}{SEPARATOR}{hashing}".encode())

    encryption = input("Encrypt file? ")
    connection.send(encryption.encode())

    if(encryption=="yes"):
        custKey = input("What would you like the key to be? ")
        connection.send(custKey.encode())

    #checking for duplicates
    dupAction=""
    dupStatus = connection.recv(BUFFER_SIZE).decode()
    if (dupStatus=="duplicate"):
        dupAction = input("There is already a file with that name, would you like to rename the file or overwrite the existing file?")
        connection.send(dupAction.encode())

   #upload_Progress = tqdm.tqdm(range(fileSize), f"Sending {file}", unit="B", unit_scale=True, unit_divisor=1024)
    
    chunkSz = 1024
    sentAmount = 0
    while sentAmount < len(data):
        sent = connection.send(data[sentAmount:sentAmount+chunkSz])
        if sent == 0:
            break
        sentAmount += sent

    if(dupAction!="rename"):
        print("File uploaded successfully.")

    #upload_Progress.update(len(data))

    connection.close()

           
            
#method used when user wants to download a file
def download():
    FileName = input("Enter the name of the file to download: ")

    connection.send(f"{FileName}".encode(FORMAT))
    cont = "cont"
    encryptionState = connection.recv(BUFFER_SIZE).decode()

    if(encryptionState=="protected"):
        giveKey = input("What is the key?\n")
        connection.send(giveKey.encode())

        cont = connection.recv(BUFFER_SIZE).decode()

    if(cont=="cont"):
        print("Correct key!")
        data = b''
        hashVal = ''
        while True:
            chunkSz = connection.recv(1024)
            if not chunkSz:
                break
            if not hashVal:
                data += chunkSz
                       
            if chunkSz.find(b''):
                hashalue += chunkSz.decode()

        recHash = hashlib.sha256(data).hexdigest()


        with open("Client_Files\\"+FileName, 'wb') as writtenFile:
            writtenFile.write(data)
            
        fileSize = os.path.getsize(str("Client_Files\\"+FileName))
        #download_Progress = tqdm.tqdm(range(fileSize), f"Downloading {FileName}", unit="B", unit_scale=True, unit_divisor=1024)
        #download_Progress.update(len(data))

        print("File downloaded successfully.")
        writtenFile.close()
    else:
        print("That is not the correct key. Unfortunately you cannot access this file.")

print("Welcome to the server! \n")


connect()
connection.send(userAct.encode())
if(userAct == "upload"):
    uploadFile()
elif(userAct == "download"):
    download()
elif(userAct == "list"):
    listFiles()
else:
    print("command not recignized")


