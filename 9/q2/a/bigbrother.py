from scapy.all import *
from math import *

FORBIDDEN_WORD = 'love'

unpersons = set()

def spy(packet):
    if packet != None:
    	if packet.haslayer(TCP):
    		payload = packet.getlayer(TCP).sprintf('%TCP.load%')
    		if FORBIDDEN_WORD in payload:
    			unpersons.add(packet.getlayer(IP).src)


def main():
    sniff(prn=spy)


if __name__ == '__main__':
    main()
