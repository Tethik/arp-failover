arp-failover
============

Simple arp failover program. Uses arp spoofing to take over IP traffic.
To accomplish this we use ARP spoofing and ICMP ping. ICMP ping is used
to detect when the host is up or down and arp spoofing to take over the
traffic when it is down.

Requirements
============
* iptables
* ifconfig
* python 2.7
* standard c libs for unix.

Installation
============
Build the c executables by running `make` in the base directory.

Usage
============
The application is actually a collection of smaller scripts used in
conjuction.

The main program is run by the `failover` bash script. It might require root
permissions.

    Usage: failover <interface> <target ip> <source ip> <target hw>
    Example: failover eth0 192.168.1.11 192.168.1.137 b8:27:eb:b1:76:df

Other scripts include:
* `failoverinit`
* `bin/ping`
* `bin/arp`
* `py-src/pingloopy.py`
* `py-src/arploopy.py`
* `py-src/failover.py`
* `py-src/arpwithmacaddress.py`


Thanks to
============
Our C code is very much based on example code authored by P.D Buchan.
You can find his great examples here:
http://www.pdbuchan.com/rawsock/rawsock.html
