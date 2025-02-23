#!/usr/bin/python

__author__ = "bt3gl"

import decimal
import socket
from constants import mod

def print_hex(secret):

    # cutting L in the end
    a = hex(secret)[:-1]

    # cutting the \x symbol
    b = a[2:].decode('hex')

    return b



def convolution(e1, e2, m2, mod):

    return (e1 * e2 )%(mod*mod)



def nc_paillier(mod):

    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))


    # answer the initial question
    s.recv(4096)
    s.send(b'paillier')
    s.recv(4096)
    m = s.recv(4096)
    m = (m.split(": ")[1]).split('\n')[0]
    mdec = decimal.Decimal(m)


    # encrypt 1
    e = '1'
    m2 = decimal.Decimal(e)
    s.send(b'E')
    s.recv(4096)
    s.send(e)
    e2 = s.recv(4096)
    e2 = e2.split(": ")[1]
    e2dec = decimal.Decimal(e2)



    # convolute the enc messages
    answer = convolution(mdec, e2dec, m2, mod)


    # get the description from the answer
    s.send(b'D')
    s.recv(4096)
    s.recv(4096)
    s.send(str(answer))
    md = s.recv(4096)
    md = md.split(": ")[1].strip()



    # get the flag, remember to add d(e(1)) = 1
    secret = long(md) + 1
    flag = print_hex(secret)
    print("The flag is: ")
    print flag





if __name__ == "__main__":

    # really long numbers
    decimal.getcontext().prec = 1240

    PORT = 12445
    HOST = 'asis-ctf.ir'

    nc_paillier(mod)





