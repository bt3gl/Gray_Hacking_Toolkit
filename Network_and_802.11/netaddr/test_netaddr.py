#!/usr/bin/env python

__author__ = "bt3gl"

import netaddr

ip = '192.168.1.114'
if ip in netaddr.IPNetwork('192.168.1.0/24'):
    print('OK!')
