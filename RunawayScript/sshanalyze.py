#!/usr/bin/python
# sshanalyze.py
# analyze stats sent by remote host to screen for potential runaway processes
# Written by Whopper
# 3/7/12
# _____________________________________________________________

import sys, os, subprocess, commands, string


class analyzer(object):

  load_ave = 0
  host = ''

  def __init__(self, hostarg):
    self.host = hostarg


  def GetLoadAve(self):
    StatFile = open('runtemp.txt')
    GetData = []
    GetData = StatFile.readlines()

    FormatData = []
    FormatData.append(GetData[2].rstrip('\r\n'))

    LoadAverage = FormatData[0]
    self.load_ave = float(LoadAverage[-4:])
    if self.load_ave > 1.5:
      self.Alert(self.host)

  def Alert(self, hostarg):


    print '_______________________________________________________________________'
    print 'Warning: High Load Average'
    print 'Machine: %s' % self.host
    print "             CPU    %usr   %nice    %sys  %iowait   %irq   %soft   %steal  %guest  %idle"
    subprocess.call(['cat runtemp.txt && echo "Users:" && echo " "\
     && ssh whopper@%s "who | sort"' % self.host], shell=True) 
    print '_______________________________________________________________________' 


if __name__ == '__main__':
  main()

