#!/usr/bin/env python

__author__ = "bt3gl"


from Crypto.Cipher import DES

def decrypt(key, text):
    des = DES.new(key, DES.MODE_ECB)
    return des.decrypt(text)

def encrypt(key, text):
    des = DES.new(key, DES.MODE_ECB)
    return des.encrypt(text)

if __name__ == '__main__':
    text = "01234567"
    key = 'abcdefgh'
    print encrypt(key, text)
    print
    print decrypt(key, text)

