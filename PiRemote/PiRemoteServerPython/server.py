import socket
import sys
import dummy_thread as _thread
import os
import signal
import pafy

def clean_exit(signum, frame):
    print 'Socket closed'
    socket.close()
    sys.exit(0)

def setup_socket(strIp,strPort):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Get Host
    HOST = socket.gethostbyname(socket.gethostname())
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((strIp, int(strPort)))
    sock.listen(1)
    print 'Started socket on ' , strIp , ' : ' , strPort
    return sock

def is_file_downloaded(strLink):
    for link in tMusicDatabase:
        if link == strLink:
            return True
    return False

# Threaded Method
def play_music(strFileName):
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
                return
		
	    strResult = process_message(data.decode('utf-8'),connection)
            #connection.sendall(bytes(strResult))
        except:
           connection.close()
           print("Connection closed")
           return


def process_message(strMsg,conn):
    print ("Processing msg", strMsg)
    video = pafy.new(strMsg)
    if video:
        os.system('killall omxplayer.bin')
        if is_file_downloaded(video.videoid):    
            conn.sendall(bytes('File found now playing'))
            os.system('omxplayer --no-keys Music/' + video.videoid + '.m4a &')
        else:
            audioStream = video.getbestaudio()
            conn.sendall(bytes('File not found ,  now downloading ' + str(audioStream.get_filesize()) + ' bytes'))
            audioStream.download('Music/' + video.videoid + '.m4a')
            conn.sendall(bytes('File downloaded , now playing'))
            tMusicDatabase.append(video.videoid)
            os.system('omxplayer --no-keys Music/' + video.videoid + '.m4a &')
    else:
        return 'Invalid link'
    conn.sendall(bytes('Task Completed'))



def start_listening(sock):
    nThreadCounter = 1
    while True:
        print ('Waiting for a connection')
        try:
            connection, client_address = sock.accept()
            _thread.start_new_thread( get_requests, (connection,client_address,nThreadCounter) )
            nThreadCounter = nThreadCounter + 1
        except:
            sock.close()
            print ("Error while creating thread")
            break


def build_database():
    tFiles = get_filenames()
    for strFile in tFiles:
        if strFile.endswith('.m4a'):
            tMusicDatabase.append(strFile[:-4])

def get_filenames():
    tNames = []
    dirList=os.listdir(os.path.dirname(os.path.realpath(sys.argv[0]))+'/Music')
    for fname in dirList:
        tNames.append(fname)
    return tNames




# Cycle
socket

tMusicDatabase = []
build_database()

#print 'Len' , len(sys.argv)
#print 'Arg1' , sys.argv[0]
#print 'Arg2' , sys.argv[1]
if len(sys.argv) == 3:
	socket = setup_socket(sys.argv[1],sys.argv[2])
else:
	socket = setup_socket('192.168.1.109',9875)

signal.signal(signal.SIGINT, clean_exit)
start_listening(socket)
socket.close()
