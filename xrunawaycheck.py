#!/usr/bin/python
# Runaway Process Locator
# Does a quick mpstat of all machines to check for CPU usage
# Written by Whopper
# 1/15/10
# _____________________________________________________________

import sys, os, subprocess, commands, string

def main():

  print '\n\nWelcome to Runaway Process Hunter. \n'
  run = raw_input('Would you like to run now? (yes or no) ')
  
  if run[0:] == 'yes':
    whichos = ''
    while whichos[0:] != 'linux' and whichos[0:] != 'unix' and whichos[0:] != 'special' and whichos[0:] != 'mini':
      whichos = raw_input('Enter \'linux\' , \'unix\' ,  \'special\', or \'mini\' (single check) ')
   
      if whichos[0:] == 'linux' or whichos [0:] == 'unix':
        if whichos[0:] == 'linux':
          boxes = open('/home/whopper/CAT/Boxes/LinuxBoxesNN')
        elif whichos[0:] == 'unix':
          boxes = open('/home/whopper/CAT/Boxes/UnixBoxes')

        boxlistuse = []
        boxlist = []
        boxlist = boxes.readlines()
        for line in boxlist:
          boxlistuse.append(line.rstrip('\r\n'))
        
        checker(boxlistuse, whichos)
      
      elif whichos[0:] == 'special':
        othercheck()
      elif whichos[0:] == 'mini':
        minichecker()
      else:
        print 'Bad input... Try again.'

  elif run[0:] == 'no':
    print 'Exiting...'


def minichecker():

  boxlist=[]
  box=raw_input('Enter box name: ')
  boxlist.append(box)
  which =''
  
  while which[0:] != 'unix' and which[0:] != 'linux' and which[0:] != 'special':
    whichos=raw_input('Enter \'unix\', \'linux\', or \'special\': ')
    if whichos[0:] == 'unix':
      checker(boxlist, whichos)
    elif whichos[0:] == 'linux':
      checker(boxlist, whichos)
    elif whichos[0:] == 'special':
      othercheck()
    else:
      print 'Bad input... try again.'

def checker(boxlist, whichos):
 
  print '\n\nBeginning Search... Will take several minutes.'
  print 'Note: No output means Load Average is normal - and no runaway present\n\n'

  i=0
  if whichos[0:] == 'linux':
    detline = 2
  elif whichos[0:] == 'unix':
    detline = 1
    
  for each in boxlist:
    subprocess.call(['echo "0.00" > runtemp.txt'], shell=True)
    subprocess.call(["ssh -o ConnectTimeout=5 whopper@%s 'mpstat 1 3 > temptest; cat temptest | grep Average' > runtemp.txt" % boxlist[i]], shell=True)
    subprocess.call(['echo " " >> runtemp.txt'], shell=True)
    subprocess.call(["ssh -o ConnectTimeout=5 whopper@%s 'uptime | cut -b 40-' >> runtemp.txt" % boxlist[i]], shell=True)
    subprocess.call(['echo " " >> runtemp.txt'], shell=True)
    subprocess.call(["ssh -o ConnectTimeout=5 whopper@%s 'ps -eo pcpu,pmem,args,time,pid,user | { head -1 ; sort -k 1 -r -n ; } | head -n 9' >> runtemp.txt" % boxlist[i]], shell=True)    
    subprocess.call(['echo " " >> runtemp.txt'], shell=True)
    subprocess.call(['echo "%s" >> runtemp.txt' % boxlist[i]], shell=True)
    
    # Alert section: Prepare file to output with high load average, or continue if fail to connect (ssh) 
    lfile = open('/home/whopper/CAT/runtemp.txt') 
    loadave = []
    loadlistb = []
    ldastring = ' '
    loadlistb = lfile.readlines()
    loadave.append(loadlistb[detline].rstrip('\r\n'))
    ldastring = loadave[0]
    if ldastring[1:] == "":
      i = i + 1
      continue
    else:
      intlda = float(ldastring[-4:]) 
      if intlda > 1.5:
        print '_______________________________________________________________________'
        print 'Warning: High Load Average'
        print 'Machine: %s' % boxlist[i]
        print "             CPU    %usr   %nice    %sys  %iowait   %irq   %soft   %steal  %guest  %idle"
        subprocess.call(["cat /home/whopper/CAT/runtemp.txt"], shell=True) 
        subprocess.call(['echo "Users:"'], shell=True)
        subprocess.call(['echo " "'], shell=True) 
        subprocess.call(["ssh whopper@%s 'who | sort'" %boxlist[i]], shell=True)
        print '_______________________________________________________________________' 

    i = i + 1

def othercheck():
  print 'Broken'
  
  
      
if __name__ == '__main__':
  main()

