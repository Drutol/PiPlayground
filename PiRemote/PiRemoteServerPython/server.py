import socket
import logging
import sys
import dummy_thread as _thread
import threading
import os
import signal
import pafy
import random
import time
from omxplayer import OMXPlayer


def clean_exit(signum, frame):
    print 'Socket closed'
    try:
        player.quit()
    except:
        print 'Closed'
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

def play_music(strID,conn):
    try:
        player.quit()
    except:
        print 'Error'
    global player 
    player = OMXPlayer('Music/' + strID + '.m4a')
    player.play()
    if conn != 'lol':
        conn.sendall(bytes('Now playing: ' +  dTitleDatabase.get(strID,strID)))
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
    print "Processing msg ", strMsg[3:]

    if strMsg == 'Pause':
        try:
            player.pause()
            conn.sendall(bytes('Playback stopped'))
        except:
            print 'Error'
        return
    
    if strMsg == 'Play':
        try:
            player.play()

        except:
            print 'Error'
        return    
    
    if strMsg == 'Stop':
        global playingRandom
        playingRandom = False       
        try:
            player.quit()
        except:
            print 'Error'
        return

    if strMsg == 'VolUP':
        try:
            player.action(18)
        except:
            print 'Error'
        return

    if strMsg == 'VolDOWN':
        try:
            player.action(17)
        except:
            print 'Error'
        return
   
   
    if strMsg == 'random':
        global playingRandom
        playingRandom = False
        play_music(random.choice(tMusicDatabase),conn)
        return
    if strMsg == 'StopServer':
        os.system('sudo halt')  
    if strMsg == 'GimmeLinks':
        strLinks = 'Links;'
        for link in tMusicDatabase:
            title = dTitleDatabase.get(link,'Title not available ' + link) 
            strLinks = strLinks + link  + '$' + title + ';'
        strLinks = strLinks + ';EOS'
        conn.sendall(bytes(strLinks))
        return
    if strMsg == 'StartRandom':
        global playingRandom
        playingRandom = True
        check_random()
        return
   
    video = None
    try:    
        video = pafy.new(strMsg)
    except:
        conn.sendall(bytes('Invalid Link'))
        return

    if video:
        global playingRandom
        playingRandom = False
        if is_file_downloaded(video.videoid):    
            play_music(video.videoid,conn)
        else:
            audioStream = video.getbestaudio()
            conn.sendall(bytes('File not found ,  now downloading ' + str(audioStream.get_filesize()) + ' bytes'))
            audioStream.download('Music/' + video.videoid + '.m4a',callback = download_callback)
            tMusicDatabase.append(video.videoid)
            play_music(video.videoid,conn)


def check_random():
    if playingRandom == True:
        play_music(random.choice(tMusicDatabase),'lol')
        threading.Timer(int(player.duration()), check_random).start()


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
            words = line.split('||')
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
        file.write(key + '||' + dTitleDatabase[key] + '\n')

    print len(dTitleDatabase) , ' links in database'




# Cycle


socket

tMusicDatabase = []
dTitleDatabase = {}
global player
global playingRandom
playingRandom = False
logging.disable(logging.CRITICAL)
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

