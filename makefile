all: arp ping

clean:
	rm bin/*

arp: src/arp.c
	gcc src/arp.c -o bin/arp

ping: src/ping.c
	gcc src/ping.c -o bin/ping
