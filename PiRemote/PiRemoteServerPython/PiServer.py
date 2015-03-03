import socket
import sys
import _thread
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
HOST = socket.gethostbyname(socket.gethostname())

server_address = (socket.gethostname(), 9875)
print("Starting listening service on", HOST)
sock.bind((HOST, 9875))
sock.listen(10)



# Threaded Method
def get_requests(connection, address, ID):
    print("Started new thread",ID)
    while True:
        try:
            data = connection.recv(512)
            print("Received message from ", address, "Thread: ", ID)
            print("Message :", data.decode('ascii'))
            strResult = process_message(data.decode('ascii'))
            connection.sendall(bytes(strResult, "utf-8"))
        finally:
            print("Connection closed")
            _thread.exit_thread()


def process_message(strMsg):
    print ("Processed msg", strMsg)
    return "Done"


def start_listening():
    nThreadCounter = 1
    while True:
        print ('Waiting for a connection')
        connection, client_address = sock.accept()
        try:
            _thread.start_new_thread( get_requests, (connection,client_address,nThreadCounter) )
            nThreadCounter = nThreadCounter + 1
        except:
            print ("Error while creating thread")


# Cycle
start_listening()