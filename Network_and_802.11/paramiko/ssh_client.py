#!/usr/bin/env python

__author__ = "bt3gl"


import paramiko
import sys
import getopt

def usage():
    print "Usage: ssh_client.py  <IP> -p <PORT> -u <USER> -c <COMMAND> -a <PASSWORD> -k <KEY> -c <COMMAND>"
    print "  -a                  password authentication"
    print "  -i                  identity file location"
    print "  -c                  command to be issued"
    print "  -p                  specify the port"
    print "  -u                  specify the username"
    print
    print "Examples:"
    print "ssh_client.py 129.49.76.26 -u buffy -p 22 -a killvampires  -c pwd"
    sys.exit()


def ssh_client(ip, port, user, passwd, key, command):
    client = paramiko.SSHClient()
    if key:
        client.load_host_keys(key)
    else:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.exec_command(command)
        print
        print ssh_session.recv(4096)


def main():

    if not len(sys.argv[1:]):
        usage()

    # parse the arguments
    IP = '0.0.0.0'
    USER = ''
    PASSWORD = ''
    KEY = ''
    COMMAND = ''
    PORT = 0

    try:
        opts = getopt.getopt(sys.argv[2:],"p:u:a:i:c:", \
            ["PORT", "USER", "PASSWORD", "KEY", "COMMAND"])[0]
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
        elif t[0] in ('-i'):
            KEY = t[1]
        elif t[0] in ('-c'):
            COMMAND = t[1]
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
    if KEY:
        print "[*] The key at %s will be used." % KEY
    if COMMAND:
        print "[*] Executing the command '%s' in the host..." % COMMAND
    else:
        print "You need to specify the command to the host."
        usage()

    # start the client
    ssh_client(IP, PORT, USER, PASSWORD, KEY, COMMAND)


if __name__ == '__main__':
    main()
