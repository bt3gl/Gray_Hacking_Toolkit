#!/usr/bin/env python


__author__ = "bt3gl"


def xor_str(str1, str2):
    flag = ""
    for i in range(len(str1)):
        flag += (chr(int(str1[i], 16) ^ int(str2[i], 16)))
    print flag


if __name__ == '__main__':
    kTXt = ''.join('28 36 38 2C 10 03 04 14 0A 15 08 14 02 07 08 18 0D 00 61 04 16 11 0B 12 00 07 61 03 0C 73 02 1F 02 1D 06 12 63 04 08 03 0B 1C 14 03 63 1D 0E 03 0A 10 04 2A 61 8F AC C1 00 00 00 00').split()
    xORk = ''.join('43 53 41 57 43 53 41 57 43 53 41 57 43 53 41 57 43 53 41 57 43 53 41 57 43 53 41 57 43 53 41 57 43 53 41 57 43 53 41 57 43 53 41 57 43 53 41 57 43 53 41 57 43 53 41 57 43 53 41 57').split()

    xor_str(kTXt, xORk)
