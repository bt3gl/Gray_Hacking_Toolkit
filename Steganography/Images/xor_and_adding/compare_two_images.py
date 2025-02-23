#!/usr/bin/env python

__author__='bt3gl'

'''
Compare two aligned images of the same size.

Usage: python compare.py first-image second-image
'''

import sys

from scipy.misc import imread, imsave


def compare_images(img1, img2):
    diff = img1 + img2  
    imsave('sum.png', diff)	
    diff = img1 - img2  
    imsave('diff.png', diff)



def main():
    file1, file2 = sys.argv[1:1+2]
    img1 = imread(file1).astype(float)
    img2 = imread(file2).astype(float)
    compare_images(img1, img2)

if __name__ == "__main__":
    main()
