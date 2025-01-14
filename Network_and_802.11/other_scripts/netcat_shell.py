#!/usr/bin/env python

__author__ = "bt3gl"


import os
from subprocess import Popen, STDOUT, PIPE

# Defining constants
SHELL_COMMAND = "nc 54.209.5.48 12345"


def next_line(stdout):
  # read inputs in lines
  line = ""
  while True:
    r = stdout.read(1)
    if r == '\n':
      break
    line += r
  return line


def write(stdin,val):
  # write outputs
  stdin.write(val)


def nl():
  # next line for iteration
  return next_line(p.stdout)


def wr(val):
  # write for iteration
  write(p.stdin,val)


def ntext():
  line = ""
  while "psifer text:" not in line:
    line = nl()
  return line[len("psifer text:") + 1:]


def main():

  p = Popen(SHELL_COMMAND, shell=True, cwd="./", stdin=PIPE,
    stdout=PIPE, stderr=STDOUT,close_fds=True)

  while True:
    text = ntext()
    text += " -> just an example"
    wr(ans + '\n')

  ret = p.wait()
  print "Return code: %d" % ret



if __name__ == '__main__':
  main()
