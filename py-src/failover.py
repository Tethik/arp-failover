#!/usr/bin/python
from pingloop import PingLoop
from arploop import ArpLoop
from arpwithmacaddress import ArpWithMacAddress
import sys, threading

'''
	ARP Failover program. Monitors a given host ip and once it detects
	the host being down it will automatically attempt to temporarily 
	take over the traffic for that host using ARP spoofing.
'''
class Failover:
	gratuitous_arp = True
	
	# Todo
	arp_spoof_replier = False
	
	def __init__(self, network_interface, src_ip, target_ip, target_MAC):
		self.monitor = PingLoop(network_interface, src_ip, target_ip)
		self.broadcaster = ArpLoop(network_interface, target_ip, target_ip)	
		self.arpResetter = ArpWithMacAddress(network_interface, target_ip, target_ip, target_MAC)	
		self.isSpoofing = False
	
	'''
		This method is called with every ping reply (or timeout). 
		event currently contains two variables: 
			* up: is the host connected?
			* time: the time taken to reply. if not up, this will be -1
	'''
	def _get_host_status(self, event):
		if not event.up:
			if self.isSpoofing:
				print "Host is still down."
				return
			
			self.isSpoofing = True
			print "# Host just went down. Starting spoof!"
			if self.gratuitous_arp:
				self.t = threading.Thread(target=self.broadcaster.start)
				self.t.deamon = True
				self.t.start()
				
			if self.arp_spoof_replier:
				pass #Todo
		else:		
			if(self.isSpoofing):
				# Todo: broadcast for original host with original hw?
				print "# Host is back up!"
				self.stopSpoofing()
		
	
	def start(self):
		try:
			self.monitor.subscribe(self._get_host_status)
			self.monitor.run()
		except KeyboardInterrupt:
			print "\nLoop interuppted by user."
			self.stopSpoofing()
			
	def stopSpoofing(self):
		if self.isSpoofing:
			print "# Stopping spoof"
			self.broadcaster.stop()
			self.arpResetter.execute()
			self.t.join()
			self.isSpoofing = False
		
		
def main(argv):	
	if(len(argv) < 5):
		print """
USAGE: failover.py <interface> <src_ip> <target_ip> <MAC-address>
Example: failover.py eth0 192.168.1.80 192.168.1.1 C2:34:0F:20:04:CC

ARP Failover program. Monitors a given host ip and once it detects
the host being down it will automatically attempt to temporarily 
take over the traffic for that host using ARP spoofing.

When host gets back online it will send out a gratitious ARP request to
reset the ARP cache to the original state.

			"""
		exit()
	
	failover = Failover(argv[1],argv[2],argv[3], argv[4])
	try:
		failover.start()
	except KeyboardInterrupt:
		print "\nLoop interuppted by user."
	
		

if __name__ == '__main__':
	main(sys.argv)

