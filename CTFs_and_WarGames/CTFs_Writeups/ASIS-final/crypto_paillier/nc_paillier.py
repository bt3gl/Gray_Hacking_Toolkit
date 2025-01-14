#!/usr/bin/python

__author__ = "bt3gl"


import decimal
import socket


def nc_paillier():

    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))


    # answer the initial question
    print s.recv(4096)
    s.send(b'paillier')


    # get the secret
    print s.recv(4096)
    m = s.recv(4096)

    # cleaning it
    m = (m.split(": ")[1]).split('\n')[0]

    # it's good to print (because it changes periodically)
    print("The secret is: ")
    print(m)

    # change from str to long decimal
    mdec = decimal.Decimal(m)


    '''
        From here you can do whatever you want.
    '''
    # If you want to encrypt messages

    msg_to_e = '1'

    s.send(b'E')
    print s.recv(4096)
    s.send(msg_to_e)
    me = s.recv(4096)
    me = me.split(": ")[1]

    print("Secret for %s is:" %(msg_to_e))
    print(me)

    medec = decimal.Decimal(me)


    # If you want to decrypt messages

    msg_to_d = me

    s.send(b'D')
    s.recv(4096)
    s.recv(4096)
    s.send(msg_to_d)
    md = s.recv(4096)
    md = md.split(": ")[1].strip()

    print("Decryption is: ")
    print(md)

    mddec = decimal.Decimal(md)





if __name__ == "__main__":
    # really long numbers
    decimal.getcontext().prec = 1240

    PORT = 12445
    HOST = 'asis-ctf.ir'

    nc_paillier()

