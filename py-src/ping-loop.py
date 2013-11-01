#!/usr/bin/python
import sys, os, subprocess, time

class PingLoop:
	# Assuming that the C program is located in the relative directory
	ping_executable = "../bin/ping"
	ping_delay = 10
	
	def __init__(self, network_interface, src_ip, target_ip):
		self.network_interface = network_interface
		self.src_ip = src_ip
		self.target_ip = target_ip
		print "# Setting up loop for pinging " + target_ip + " (with " + src_ip + " on " + network_interface + ") "
	
	def executableExists(self):
		return os.path.isfile(self.ping_executable)
		
	def run(self):
		print "# Starting loop."
		while True:
			subprocess.call([self.ping_executable, self.network_interface, self.src_ip, self.target_ip], stdout=sys.stdout);
			time.sleep(self.ping_delay)		


def main(argv):	
	if(len(argv) < 3):
		print "USAGE: ping-loop.py <interface> <src_ip> <target_ip>"
		print "Example: ping-loop.py eth0 192.168.1.80 192.168.1.1"
		print 
		print "Note: only works on local networks (private). The ping program currently only pings the broadcast MAC address."
		exit()
	
	plopp = PingLoop(argv[1],argv[2],argv[3])
	if(not plopp.executableExists()):
		print "Missing C program to ping with. Make sure you've built the raw socket programs."
		exit(1)
	
	try:
		plopp.run()
	except KeyboardInterrupt:
		print "\nLoop interuppted by user."
	
		

if __name__ == '__main__':
	main(sys.argv)
