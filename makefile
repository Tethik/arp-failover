all: arp ping

clean:
	rm arp ping

arp: arp.c
	gcc arp.c -o arp

ping: ping.c
	gcc ping.c -o ping
