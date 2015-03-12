import socket
import sys
import dummy_thread as _thread
import os
import signal
import pafy
import random
import time

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
	    process_message(data.decode('utf-8'),connection)
       except:
           connection.close()
           print("Connection closed")
           return


callbackConnetion = None
# Dl Callback function
def download_callback(total, recvd, ratio, rate, eta):
    if int(total)/4 == int(recvd)or int(total)/2 == int(recvd):
        if callbackConnection:
            callbackConnection.sendall(bytes('DL ETA: ' + str(eta)))


def process_message(strMsg,conn):
    print ("Processing msg", strMsg)
    if strMsg == "Play" and strPreviousTrack != None:
        os.system('killall oxmplayer.bin')
        os.system('omxplayer --no-keys Music/' + strPreviousTrack + '.m4a &')
        conn.sendall(bytes('Now playing'))
        return
    elif strMsg == 'Play' and strPreviousTrack is None:
        conn.sendall(bytes('No track to play'))
        return     

    if strMsg == 'Pause':
        os.system('killall omxplayer.bin')
        conn.sendall(bytes('Playback stopped'))
        return
   
    if strMsg == 'random':
        os.system('killall omxplayer.bin')
        os.system('omxplayer --no-keys Music/' + random.choice(tMusicDatabase) + '.m4a &')
        return
  
    if strMsg == 'GimmeLinks':
        strLinks = 'Links;'
        for link in tMusicDatabase:
            title = dTitleDatabase.get(link,'Title not available ' + link) 
            strLinks = strLinks + link  + '|' + title + ';'
        conn.sendall(bytes(strLinks))
        return


    video = None
    try:    
        video = pafy.new(strMsg)
    except:
        conn.sendall(bytes('Invalid Link'))
        return

    if video:
        os.system('killall omxplayer.bin')
        if is_file_downloaded(video.videoid):    
            conn.sendall(bytes('File found now playing'))
            os.system('omxplayer --no-keys Music/' + video.videoid + '.m4a &')
            strPreviousTrack = video.videoid
        else:
            audioStream = video.getbestaudio()
            conn.sendall(bytes('File not found ,  now downloading ' + str(audioStream.get_filesize()) + ' bytes'))
            callbackConnection = conn
            audioStream.download('Music/' + video.videoid + '.m4a',callback = download_callback)
            callbackConnection = None
            conn.sendall(bytes('File downloaded , now playing'))
            tMusicDatabase.append(video.videoid)
            os.system('omxplayer --no-keys Music/' + video.videoid + '.m4a &')
            strPreviousTrack = video.videoid



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

def build_titledatabase():
    file = None
    try:
        file = open("Music/TitleDB.txt",'r')
        for line in file:
            words = line.split('|')
            if len(words) == 2:
                dTitleDatabase[words[0]] = words[1]
    except:
        print 'Error reading file'

    for link in tMusicDatabase:
        if dTitleDatabase.get(link) == None:
            print 'Getting title for ' , link
            vid = pafy.new(link)
            dTitleDatabase[link] = vid.title
            time.sleep(0.1)
   
    if file != None:
        file.close()
    file = open("Music/TitleDB.txt","w")
    
    tKeys = dTitleDatabase.keys()
    
    for key in tKeys:
        file.write(key + '|' + dTitleDatabase[key] + '\n')

    print len(dTitleDatabase) , ' links in database'




# Cycle
socket

tMusicDatabase = []
dTitleDatabase = {}
build_database()
build_titledatabase()
strPreviousTrack = None
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
