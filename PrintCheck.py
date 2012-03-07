#!/usr/local/bin/python
# FAB/EB printer Test Script
# Sends randomly generated pages to printers specified by a ticket.
# Rewrite of original bash script
# Written by Whopper
# 11/18/10 :: 12/20/10
# _______________________________________________________________________

import sys, os, subprocess, commands, re

def main():
	
	Ticknum = raw_input('Please enter ticket number now, (\'mini\' for individual test or \'queue\' for queue check): ')
	match = re.search(r'\d', Ticknum[0:])

	if match:
		decision(Ticknum)
	else:
		if Ticknum[0:] == 'mini':
			minitest()
		elif Ticknum[0:] == 'queue':
			queue()
		else: 
			print 'Invalid input, defaulting to queue check.'
			queue()

# Decision function ================================================================================== 
def decision(Ticknum):
	Testtic = commands.getoutput("snot -s %s | grep -w -c 'FAB'" % Ticknum)

	# EB SECTION
	if Testtic == "0": 
		print 'This ticket is for EB printers.'
		PrintnamesList =['eb325bw1', 'eb325bw2', 'eb423bw1']
		TGen(PrintnamesList)

	# FAB SECTION 
	elif Testtic > "0":
		print 'This ticket is for FAB printers.'	 
		PrintnamesList =['fab5517bw1', 'fab5517bw2', 'fab6001bw1', 'fab6019bw1', 'fab8201bw1']
		TGen(PrintnamesList)
# End Decision Function ================================================================================== 

# MiniTest function ___________________________________________________________________________________
def minitest():
	
	k = 0
	PrintnamesList = []
	numprint = raw_input('Please enter the number of printers needed: ')
	numprint = int(numprint)
	while k < numprint:
		printer = raw_input('Please enter printer name now: ')
		PrintnamesList.append(printer)
		k = k + 1
	TGen(PrintnamesList)
# End MiniTest function _______________________________________________________________________________	

# Test Page gen function ______________________________________________________________________________
def TGen(PrintnamesList):
	i = 0
	print 'Sending test pages to: ', PrintnamesList
	for each in PrintnamesList:
		subprocess.call(["cat /dev/urandom | tr -cd '\43-\173' | head --bytes=4980 | fold | sed '$d' > TestPage"], shell=True)
		subprocess.call(["echo -n 'AABCDEFGHIJMNOPQRST Sent by Whopper ' >> TestPage"], shell=True)
		subprocess.call(["echo -n `date` >> TestPage"], shell=True)
		subprocess.call(["echo -n ' ' %s >> TestPage" % PrintnamesList[i]], shell=True)
		subprocess.call(["lpr -P %s TestPage" % PrintnamesList[i]], shell=True)	
 		subprocess.call(["rm TestPage"], shell=True)
		i = i + 1
# ______________________________________________________________________________________________________

# Queue check function _________________________________________________________________________________
def queue():
	ebqueue = ['eb325bw1', 'eb325bw2', 'eb325clr1', 'eb423bw1', 'eb423clr1']
	fabqueue = ['fab5517clr1', 'fab5517bw1', 'fab5517bw2', 'fab6001bw1', 'fab6019bw1', 'fab8201bw1', 'fab8202bw1']

	selection = raw_input('Which printers? (eb/fab/all) ')
	if selection[0:] == 'eb':
		queue = ebqueue
	elif selection[0:] == 'fab':
		queue = fabqueue
	elif selection[0:] == 'all':
		queue = ebqueue[0:] + fabqueue[0:]
	else:
		print 'Invalid Input!'

	for each in queue:
		subprocess.call(["echo %s | xargs -n 1 lpq -P" %each], shell=True)
# End Queue check function ____________________________________________________________________________



if __name__ == '__main__':
  main()

