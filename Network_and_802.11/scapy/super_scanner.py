#!/usr/bin/env python

__author__ = "bt3gl"

from scapy.all import *
import netaddr
import random

RANGE = "192.168.1.0/24"
PORTS = [22, 23, 80, 443, 449]
CODES = [1, 2, 3, 9, 10, 13]
RANGE_IP = netaddr.IPNetwork(RANGE)


def port_scanner(host, ports):
    for dstPort in ports:
        srcPort = random.randint(1025,65534)
        resp = sr1(IP(dst=host)/TCP(sport=srcPort,dport=dstPort,flags="S"),timeout=1,verbose=0)

        if (str(type(resp)) == "<type 'NoneType'>"):
            print host + ":" + str(dstPort) + " is filtered (dropped)."

        elif(resp.haslayer(TCP)):

            if(resp.getlayer(TCP).flags == 0x12):
                send_rst = sr(IP(dst=host)/TCP(sport=srcPort, dport=dstPort, flags="R"),\
                    timeout=1, verbose=0)
                print host + ":" + str(dstPort) + " is open."

            elif (resp.getlayer(TCP).flags == 0x14):
                print host + ":" + str(dstPort) + " is closed."

            elif(resp.haslayer(ICMP)):
                if(int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) in \
                    CODES):
                    print host + ":" + str(dstPort) + " is filtered  dropped)."


def super_scanner():
    liveCounter = 0
    for addr in RANGE_IP:
        if (addr == RANGE_IP.network or addr == RANGE_IP.broadcast):
            continue

        resp = sr1(IP(dst=str(addr))/ICMP(), timeout=2, verbose=0)
        if (str(type(resp)) == "<type 'NoneType'>"):
            print str(addr) + " is down or not responding."

        elif (int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) in CODES):
            print str(addr) + " is blocking ICMP."

        else:
            port_scanner(str(addr),PORTS)
            liveCounter += 1

    print "Scanned hosts: " + str(RANGE_IP.size)
    print "Online hosts: " + str(liveCounter)


if __name__ == '__main__':
    super_scanner()
