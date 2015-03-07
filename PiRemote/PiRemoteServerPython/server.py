import socket
import sys
import dummy_thread as _thread
import os
import signal
# Create a TCP/IP socket

def clean_exit(signum, frame):
    socket.close()
    sys.exit(0)

def setup_socket(strIp,strPort):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Get Host
    HOST = socket.gethostbyname(socket.gethostname())
    sock.bind((strIp, int(strPort)))
    sock.listen(1)
    print 'Started socket on ' , strIp , ' : ' , strPort
    return sock

# Threaded Method
def play_music(strFileName):
	os.system("omxplayer out.mp3")
	_thread.exit_thread()
	return
	

# Threaded Method
def get_requests(connection, address, ID):
    print("Started new thread",ID)
    while True:
        try:
            data = connection.recv(512)
            print("Received message from ", address, "Thread: ", ID)
            print("Message :", data.decode('utf-8'))
            if data.decode("utf-8") == "Close Connection":
                print("Signal to close connection")
                _thread.exit_thread()
		
	    strResult = process_message(data.decode('utf-8'))
            connection.sendall(bytes(strResult))
        except:
            print("Connection closed")
            return


def process_message(strMsg):
    print ("Processed msg", strMsg)
    _thread.start_new_thread(play_music,("lolo",))
    return "Done"


def start_listening(sock):
    nThreadCounter = 1
    while True:
        print ('Waiting for a connection')
        connection, client_address = sock.accept()
        try:
            _thread.start_new_thread( get_requests, (connection,client_address,nThreadCounter) )
            nThreadCounter = nThreadCounter + 1
        except:
            print ("Error while creating thread")


def read_database():
    file = open('databse.txt','r')
    if file:
        for line in file:
            tMusicDatabase.append(line)




# Cycle
socket
tMusicDatabase = {}
#print 'Len' , len(sys.argv)
#print 'Arg1' , sys.argv[0]
#print 'Arg2' , sys.argv[1]
if len(sys.argv) == 3:
	socket = setup_socket(sys.argv[1],sys.argv[2])
else:
	socket = setup_socket('192.168.1.109',9875)

signal.signal(signal.SIGINT, clean_exit)
start_listening(socket)
