from scapy.all import *

FORBIDDEN_WORD = 'love'

unpersons = set()


def spy(packet):
    if packet != None:
    	if packet.haslayer(TCP):
    		if FORBIDDEN_WORD in packet.getlayer(TCP).sprintf('%TCP.load%'):
    			unpersons.add(packet.getlayer(IP).src)
    print(unpersons)


def main():
    sniff(prn=spy)


if __name__ == '__main__':
    main()
