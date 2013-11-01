#!/usr/bin/python
import sys, os, subprocess, time
from observable import Observable
from executable import Executable

class PingLoop(Observable, Executable):
	# Assuming that the C program is located in the relative directory
	ping_executable = "../bin/ping"
	ping_delay = 10
	
	def __init__(self, network_interface, src_ip, target_ip):
		Observable.__init__(self)
		Executable.__init__(self, self.ping_executable)
		self.network_interface = network_interface
		self.src_ip = src_ip
		self.target_ip = target_ip
		print "# Setting up loop for pinging " + target_ip + " (with " + src_ip + " on " + network_interface + ") "
		
	def run(self):
		print "# Starting loop."
		while True:
			result = self.execute(self.network_interface, self.src_ip, self.target_ip)
			print result
			self.fire(time=500, up=True)
			time.sleep(self.ping_delay)	
			

def printPingResult(event):
	print "Host is up: " + str(event.up)
	print "Time:" + str(event.time)

def main(argv):	
	if(len(argv) < 4):
		print "USAGE: ping-loop.py <interface> <src_ip> <target_ip>"
		print "Example: ping-loop.py eth0 192.168.1.80 192.168.1.1"
		print 
		print "Note: only works on local networks (private). The C ping program currently only pings the broadcast MAC address."
		exit()
	
	plopp = PingLoop(argv[1],argv[2],argv[3])
	plopp.subscribe(printPingResult)
	if(not plopp.executableExists()):
		print "Missing C program to ping with. Make sure you've built the raw socket programs."
		exit(1)
	
	try:
		plopp.run()
	except KeyboardInterrupt:
		print "\nLoop interuppted by user."
	
		

if __name__ == '__main__':
	main(sys.argv)
