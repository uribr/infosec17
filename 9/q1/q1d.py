from scapy.all import *
from time import *
from heapq import *

SYN_FLAG = 'S'
ACK_FLAG = 'A'
def on_packet(packet):
	tcp = packet.getlayer(TCP)
	ip = packet.getlayer(IP)
	# Generate an SA TCP packet to continue the 3-way handshake
	cyber_ninja_packet = IP(dst = ip.src) / TCP(dport = tcp.sport, sport = tcp.dport, flags = SYN_FLAG + ACK_FLAG) / Raw('')
	# Send the packet, note that if the sender is not running a SYN scanner then the next packet
	# he/she will send will be a A TCP packet (Maybe containing data aswell) and so our filtering will leave it alone.
	print(cyber_ninja_packet.show())
	send(cyber_ninja_packet, verbose = False)


def is_syn_packet(packet):
	# Similar to the beginning of on_packet(packet) in q1b.py.
	if packet != None:
		if packet.haslayer(TCP):
			tcp = packet.getlayer(TCP)
			ip = packet.getlayer(IP)
			if SYN_FLAG in tcp.sprintf('%TCP.flags%'):
				print('Got syn packet from:' + packet.getlayer(IP).src)
				return True
	return False

def main():
    sniff(lfilter = is_syn_packet, prn = on_packet)


if __name__ == '__main__':
    main()