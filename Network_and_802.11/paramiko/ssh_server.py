#!/usr/bin/env python

__author__ = "bt3gl"


import paramiko
import getopt
import threading
import sys
import socket

HOST_KEY = paramiko.RSAKey(filename='test_rsa.key')
USERNAME = 'buffy'
PASSWORD = 'killvampires'


class Server(paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == USERNAME) and (password == PASSWORD):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


def main():

    if not len(sys.argv[1:]):
        print "Usage: ssh_server.py <SERVER>  <PORT>"
        sys.exit(0)

    # creating a socket object
    server = sys.argv[1]
    ssh_port = int(sys.argv[2])
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print "[+] Listening for connection ..."
        client, addr = sock.accept()
    except Exception, e:
        print "[-] Connection Failed: " + str(e)
        sys.exit(1)
    print "[+] Connection Established!"


    # creating a paramiko object
    try:
        Session = paramiko.Transport(client)
        Session.add_server_key(HOST_KEY)
        paramiko.util.log_to_file("filename.log")
        server = Server()
        try:
            Session.start_server(server=server)
        except paramiko.SSHException, x:
            print '[-] SSH negotiation failed.'


        chan = Session.accept(10)

        print '[+] Authenticated!'
        chan.send("Welcome to Buffy's SSH")
        while 1:
            try:
                command = raw_input("Enter command: ").strip('\n')
                if command != 'exit':
                    chan.send(command)
                    print chan.recv(1024) + '\n'
                else:
                    chan.send('exit')
                    print '[*] Exiting ...'
                    session.close()
                    raise Exception('exit')
            except KeyboardInterrupt:
                session.close()


    except Exception, e:
        print "[-] Caught exception: " + str(e)
        try:
            session.close()
        except:
            pass
        sys.exit(1)




if __name__ == '__main__':
    main()
