#!/usr/bin/python
# Runaway Process Locator
# Does a quick mpstat of all machines to check for CPU usage
# Written by Whopper
# 1/15/10
# _____________________________________________________________

import sys, os, subprocess, commands, string, sshcmds, sshanalyze

def main():

  if (len(sys.argv) > 1):
      if( sys.argv[1] == '--full' ):
          print "Executing full scan...!"

          boxes    = open('/home/whopper/CAT/Boxes/LinuxBoxesNN')
          BoxList  = []
          getBoxes = []

          getBoxes = boxes.readlines()
          for line in getBoxes:
            BoxList.append(line.rstrip('\r\n'))

          checker(BoxList)

      elif( sys.argv[1] == '--mini' ):
          print "Executing single scan...!"
          minichecker()

      else:
          print "Error: Invalid Arguments Provided"
  else:
      print "Error: No Arguments Specified"
      print "Flags:\n"
      print "Full scan:      --full"
      print "Single scan:    --mini\n"

def minichecker():

  BoxList = []
  Box     = raw_input('Enter FQDN of the machine to scan: ')

  BoxList.append(Box)
  checker(BoxList)

def checker(BoxList):

  print '\n\nBeginning Search... Will take several minutes.'
  print 'Note: No output means no runaway present\n\n'


  # Initiate connection and begin scan
  i = 0

  for each in BoxList:
    s = sshcmds.remote(str(BoxList[i]))
    a = sshanalyze.analyzer(BoxList[i])

    s.execute('mpstat 1 3 > temptest; cat temptest | grep Average > runtemp.txt; echo " " >> runtemp.txt')
    s.execute('uptime | cut -b 40- >> runtemp.txt; echo " " >> runtemp.txt')
    s.execute('ps -eo pcpu,pmem,args,time,pid,user | { head -1 ; sort -k 1 -r -n ; } | head -n 9 >> runtemp.txt')
    s.execute('echo " " >> runtemp.txt && echo %s >> runtemp.txt' %BoxList[i])

    s.get('/u/whopper/runtemp.txt')
    a.GetLoadAve()
    i = i + 1


if __name__ == '__main__':
  main()

