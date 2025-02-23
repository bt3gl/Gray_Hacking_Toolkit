#!/usr/bin/env python

__author__ = "bt3gl"

from scapy.all import *

def conversation():
     p = readpcap("myfile.pcap")
     p.conversations(type="jpg", target="> test.jpg")

def simple_graph():
    res,unans = traceroute(["www.google.com", "www.yahoo.com"], dport=[80,443], maxttl=20, retry=-2)
    res.graph()
    res.graph(type="ps")
    res.graph(target="> example.png")

def ttd_graph():
    p = IP()/ICMP()
    p.pdfdump("test.pdf")

def td_graph():
    a,u = traceroute(["www.python.org", "google.com","slashdot.org"])
    a.trace3D()

def simple_plot():
    p = sniff(count=50)
    p.plot(lambda x:len(x))

if __name__ == '__main__':
    simple_plot()
