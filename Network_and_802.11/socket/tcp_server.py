#!/usr/bin/env python

__author__ = "bt3gl"


import socket
import threading

# Defining constants
# The IP address and port we want the server to listen on
BIND_IP = '0.0.0.0'
BIND_PORT = 9090


# Start a thread to handle client connection
def handle_client(client_socket):

    # Get data from client
    request = client_socket.recv(1024)
    print "[*] Received: " + request

    # Send back a packet
    client_socket.send('ACK')

    client_socket.close()



def tcp_server():

    # Create a socket object (just like the client)
    server = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

    # Start listening
    server.bind(( BIND_IP, BIND_PORT))

    # the maximum backlog of connections is set to 5
    server.listen(5)
    print"[*] Listening on %s:%d" % (BIND_IP, BIND_PORT)

    # putting the server in the loop to wait for incoming connections
    while 1:

        # when a client connects, we receive the client socket (client variable)
        # the connections variables go to the addr variable
        client, addr = server.accept()
        print "[*] Accepted connection from: %s:%d" %(addr[0], addr[1])

        # create a thread object that points to our function
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()



if __name__ == '__main__':
    tcp_server()
