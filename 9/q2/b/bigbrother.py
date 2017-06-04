from scapy.all import *
from math import *

FORBIDDEN_WORD = 'love'

unpersons = set()


def shanon_entropy(string):
	count = dict([(char, (lambda x : 0)(char)) for char in string])
	count = dict([(char, (lambda x : count[x] + 1)(char)) for char in string])

	distribution = [float(count[char]) / len(string) for char in set(string)]

	return -sum((p * (log(p)/log(2.0)) for p in distribution))


def spy(packet):
    if packet != None:
    	if packet.haslayer(TCP):
    		payload = packet.getlayer(TCP).sprintf('%TCP.load%')
    		entropy = shanon_entropy(payload)
    		if FORBIDDEN_WORD in payload or entropy > 3.0:
    			unpersons.add(packet.getlayer(IP).src)
    			print(unpersons)


def main():
    sniff(prn=spy)


if __name__ == '__main__':
    main()
