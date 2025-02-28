# Building a UDP Scanner (by bt3)

When it comes to the reconnaissance of some target network, the start point is undoubtedly on host discovering. This task might come together with the ability to sniff and parse the packets flying in the network.

What if you don't have Wireshark available to monitor a network traffic?

Again, Python comes with several solutions and today I'm going  through the steps to build a **UDP Host discovery tool**. First, we are going to see how we deal with [raw sockets](http://en.wikipedia.org/wiki/Raw_socket) to  write a simple sniffer, which is able to view and decode network packets. Then we are going to multithread this process within a subnet, which will result in our scanner.

The cool thing about **raw sockets** is that they allow access to low-level networking information. For example, we can use it to check IP and ICMP headers, which are in the layer 3 of the OSI model (the network layer).

The cool thing about using **UDP datagrams** is that, differently from TCP, they do not bring much overhead when sent across an entire subnet (remember the TCP [handshaking](http://www.inetdaemon.com/tutorials/internet/tcp/3-way_handshake.shtml)). All we need to do is wait for the ICMP responses saying whether the hosts are available or closed (unreachable).


----

##  Writing a Packet Sniffing

We start with a very simple task: with Python's socket library, we will write a very simple packet sniffer.

In this sniffer we create a raw socket and then we bind it to the public interface. The interface should be in **promiscuous mode**, which means that every packet that the network card sees are captured, even those that are not destined to the host.

One detail to remember is that things are slightly different if we are using Windows: in this case we need to send a [IOCTL](http://en.wikipedia.org/wiki/Ioctl) package to set the interface to **promiscuous mode**. In addition, while Linux needs to use ICMP, Windows allow us to sniff the incoming packets independently of the protocol:


```python
import socket
import os

# host to listen
HOST = '192.168.1.114'

def sniffing(host, win, socket_prot):
    while 1:
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_prot)
        sniffer.bind((host, 0))

        # include the IP headers in the captured packets
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if win == 1:
            sniffer.ioctl(socket.SIO_RCVALL, socket_RCVALL_ON)

        # read in a single packet
        print sniffer.recvfrom(65565)

def main(host):
    OS = os.name
    if OS == 'nt':
        socket_prot = socket.IPPROTO_IP
        sniffing(host, 1, socket_prot)
    else:
        socket_prot = socket.IPPROTO_ICMP
        sniffing(host, 0, socket_prot)

if __name__ == '__main__':
    main(HOST)
```

To test this script, we run the following command in one terminal window:
```sh
$ sudo python sniffer.py
```

Then, in a second  window, we can  [ping](http://en.wikipedia.org/wiki/Ping_(networking_utility)) or [traceroute](http://en.wikipedia.org/wiki/Traceroute) some address, for example www.google.com. The results will look like this:

```sh
$ sudo python raw_socket.py
('E\x00\x00T\xb3\xec\x00\x005\x01\xe4\x13J}\xe1\x11\xc0\xa8\x01r\x00\x00v\xdfx\xa2\x00\x01sr\x98T\x00\x00\x00\x008\xe3\r\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567', ('74.125.225.17', 0))
('E\x00\x00T\xb4\x1b\x00\x005\x01\xe3\xe4J}\xe1\x11\xc0\xa8\x01r\x00\x00~\xd7x\xa2\x00\x02tr\x98T\x00\x00\x00\x00/\xea\r\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567', ('74.125.225.17', 0))
```

Now it's pretty obvious that we need to decode these headers.

----

## Decoding the IP and ICMP Layers

A typical IP header has the following structure, where each field belongs to a variable (this header is originally [written in C](http://minirighi.sourceforge.net/html/structip.html)):

![](http://i.imgur.com/3fmVLJS.jpg)


In the same way, ICMP can vary in its content but each message contains three elements that are consistent: **type** and **code** (tells the receiving host what type of ICMP message is arriving for decoding) and **checksum** fields.

![](http://i.imgur.com/gsUPKRa.gif)


For our scanner, we are looking for a **type value of 3** and a **code value of 3**, which are the **Destination Unreachable** class and **Port Unreachable** [error in ICMP messages](http://en.wikipedia.org/wiki/Internet_Control_Message_Protocol#Control_messages).


To represent this header, we create a class, with the help of Python's [ctypes](https://docs.python.org/2/library/ctypes.html) library:

```python
import ctypes

class ICMP(ctypes.Structure):
    _fields_ = [
    ('type',        ctypes.c_ubyte),
    ('code',        ctypes.c_ubyte),
    ('checksum',    ctypes.c_ushort),
    ('unused',      ctypes.c_ushort),
    ('next_hop_mtu',ctypes.c_ushort)
    ]

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass
```

Now we are ready to write our IP/ICMP header decoder. The script below creates a sniffer socket (just as we did before) and then it runs a loop to continually read in packets and decode their information.

Notice that for the IP header, the code reads the packet, unpacks the first 20 bytes to the raw buffer, and then prints the header variables. The ICMP header data comes right after it:

```python
import socket
import os
import struct
import ctypes
from ICMPHeader import ICMP

# host to listen on
HOST = '192.168.1.114'

def main():
    socket_protocol = socket.IPPROTO_ICMP
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind(( HOST, 0 ))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    while 1:
        raw_buffer = sniffer.recvfrom(65565)[0]
        ip_header = raw_buffer[0:20]
        iph = struct.unpack('!BBHHHBBH4s4s' , ip_header)

        # Create our IP structure
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);

        print 'IP -> Version:' + str(version) + ', Header Length:' + str(ihl) + \
        ', TTL:' + str(ttl) + ', Protocol:' + str(protocol) + ', Source:'\
         + str(s_addr) + ', Destination:' + str(d_addr)

        # Create our ICMP structure
        buf = raw_buffer[iph_length:iph_length + ctypes.sizeof(ICMP)]
        icmp_header = ICMP(buf)

        print "ICMP -> Type:%d, Code:%d" %(icmp_header.type, icmp_header.code) + '\n'

if __name__ == '__main__':
    main()
```

Running the script in one terminal and sending a **ping**  in other will return something like this (notice the ICMP type 0):

```sh
$ ping www.google.com
PING www.google.com (74.125.226.16) 56(84) bytes of data.
64 bytes from lga15s42-in-f16.1e100.net (74.125.226.16): icmp_seq=1 ttl=56 time=15.7 ms
64 bytes from lga15s42-in-f16.1e100.net (74.125.226.16): icmp_seq=2 ttl=56 time=15.0 ms
(...)
```

```sh
$ sudo python ip_header_decode.py
IP -> Version:4, Header Length:5, TTL:56, Protocol:1, Source:74.125.226.16, Destination:192.168.1.114
ICMP -> Type:0, Code:0
IP -> Version:4, Header Length:5, TTL:56, Protocol:1, Source:74.125.226.16, Destination:192.168.1.114
ICMP -> Type:0, Code:0
(...)
```

In the other hand, if we run **traceroute** instead:
```sh
$ traceroute www.google.com
traceroute to www.google.com (74.125.226.50), 30 hops max, 60 byte packets
 1  * * *
 2  * * *
 3  67.59.255.137 (67.59.255.137)  17.183 ms 67.59.255.129 (67.59.255.129)  70.563 ms 67.59.255.137 (67.59.255.137)  21.480 ms
 4  451be075.cst.lightpath.net (65.19.99.117)  14.639 ms rtr102.wan.hcvlny.cv.net (65.19.99.205)  24.086 ms 451be075.cst.lightpath.net (65.19.107.117)  24.025 ms
 5  64.15.3.246 (64.15.3.246)  24.005 ms 64.15.0.218 (64.15.0.218)  23.961 ms 451be0c2.cst.lightpath.net (65.19.120.194)  23.935 ms
 6  72.14.215.203 (72.14.215.203)  23.872 ms  46.943 ms *
 7  216.239.50.141 (216.239.50.141)  48.906 ms  46.138 ms  46.122 ms
 8  209.85.245.179 (209.85.245.179)  46.108 ms  46.095 ms  46.074 ms
 9  lga15s43-in-f18.1e100.net (74.125.226.50)  45.997 ms  19.507 ms  16.607 ms

```
We get something like this (notice the several types of ICMP responses):
```sh
sudo python ip_header_decode.py
IP -> Version:4, Header Length:5, TTL:252, Protocol:1, Source:65.19.99.117, Destination:192.168.1.114
ICMP -> Type:11, Code:0
(...)
IP -> Version:4, Header Length:5, TTL:250, Protocol:1, Source:72.14.215.203, Destination:192.168.1.114
ICMP -> Type:11, Code:0
IP -> Version:4, Header Length:5, TTL:56, Protocol:1, Source:74.125.226.50, Destination:192.168.1.114
ICMP -> Type:3, Code:3
IP -> Version:4, Header Length:5, TTL:249, Protocol:1, Source:216.239.50.141, Destination:192.168.1.114
ICMP -> Type:11, Code:0
(...)
IP -> Version:4, Header Length:5, TTL:56, Protocol:1, Source:74.125.226.50, Destination:192.168.1.114
ICMP -> Type:3, Code:3
```




------
## Writing the Scanner

### Installing netaddr

We are ready to write our full scanner. First, let's install [netaddr](https://pypi.python.org/pypi/netaddr). This library allows to use a subnet mask such as 192.168.1.0/24:

```sh
$ sudo pip install netaddr
```

We can quickly test this library with the following snippet (which should print "OK"):
```python
import netaddr

ip = '192.168.1.114'
if ip in netaddr.IPNetwork('192.168.1.0/24'):
    print('OK!')
```

### Writing the Scanner

To write our scanner we are going to put together everything we have, and then add a loop to spray UDP datagrams with a string signature to all the address within our target subnet.

To make this work, each packet will be sent in a separated thread, to make sure that we are not interfering with the sniff responses:

```python
import threading
import time
import socket
import os
import struct
from netaddr import IPNetwork, IPAddress
from ICMPHeader import ICMP
import ctypes

# host to listen on
HOST = '192.168.1.114'
# subnet to target (iterates through all IP address in this subnet)
SUBNET = '192.168.1.0/24'
# string signature
MESSAGE = 'hellooooo'

# sprays out the udp datagram
def udp_sender(SUBNET, MESSAGE):
    time.sleep(5)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for ip in IPNetwork(SUBNET):
        try:
            sender.sendto(MESSAGE, ("%s" % ip, 65212))
        except:
            pass

def main():
    t = threading.Thread(target=udp_sender, args=(SUBNET, MESSAGE))
    t.start()

    socket_protocol = socket.IPPROTO_ICMP
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind(( HOST, 0 ))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # continually read in packets and parse their information
    while 1:
        raw_buffer = sniffer.recvfrom(65565)[0]
        ip_header = raw_buffer[0:20]
        iph = struct.unpack('!BBHHHBBH4s4s' , ip_header)

        # Create our IP structure
        version_ihl = iph[0]
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        src_addr = socket.inet_ntoa(iph[8]);

        # Create our ICMP structure
        buf = raw_buffer[iph_length:iph_length + ctypes.sizeof(ICMP)]
        icmp_header = ICMP(buf)

        # check for the type 3 and code and within our target subnet
        if icmp_header.code == 3 and icmp_header.type == 3:
            if IPAddress(src_addr) in IPNetwork(SUBNET):
                if raw_buffer[len(raw_buffer) - len(MESSAGE):] == MESSAGE:
                    print("Host up: %s" % src_addr)

if __name__ == '__main__':
    main()
```

Finally, running the scanner  gives a result similar to this:
```sh
$ sudo python scanner.py
Host up: 192.168.1.114
(...)
```

Pretty neat!

By the way, the results from our scanner can be checked against the values of the IP addresses in your router's **DHCP table**. They should match!

