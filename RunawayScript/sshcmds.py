#!/usr/bin/python
# ssh.py
# ssh functions: put, get, and execute
# Written by Whopper
# 3/7/12
# _____________________________________________________________


import sys, os, subprocess, commands, string

class remote(object):

  host = ''

  def __init__(self, hostarg):
    self.host = hostarg

  # push local files to a remote machine
  def get(self, remote_path):

    subprocess.call(["scp whopper@rita.cat.pdx.edu:%s ." % remote_path ], shell=True)

  # pull files from a remote machine
  def put(self, local_file, remote_path):

    subprocess.call(["scp %s whopper@rita.cat.pdx.edu:%s" % (local_file, remote_path)], shell=True)

  # execute command on a remote machine
  def execute(self, command):
    subprocess.call(["ssh -o ConnectTimeout=5 whopper@%s '%s'" % (self.host, command)], shell=True)


if __name__ == '__main__':
  main()

