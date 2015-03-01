import socket
import sys
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
HOST = socket.gethostbyname(socket.gethostname())   

server_address = (socket.gethostname(), 9875)
print(HOST)
#print ('starting up on %s port %s' % server_address)
#sock.bind(server_address)
sock.bind((HOST, 9875))
sock.listen(1)
while True:
    print ('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print ('client connected:', client_address)
        while True:
            data = connection.recv(512)
            print ('received "%s"' % data.decode('ascii'))
            if data:
	      webbrowser.open_new_tab(data.decode('ascii'))
                connection.sendall(bytes('Got It','utf-8'))
            else:
                break
    finally:
        connection.close()