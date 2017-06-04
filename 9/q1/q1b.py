from scapy.all import *
from time import *
from heapq import *


SIZE = 'queue-size'
BLOCKED = 'is-blocked'
QUEUE = 'minimum-heap'
SYN_FLAG = 'S'
MAX_SYNS_ALLOWED_IN_TIME_INTERVAL = 15
TIME_INTERVAL = 60 
HOST = '10.0.2.15'
syn_counting_table = dict()


def on_packet(packet):
	time_of_arrival = time()

	if packet != None and packet.haslayer(TCP): # Is non-empty and is a TCP\IP packet?

		ip_addr = packet.getlayer(IP).src

		if False == is_blocked(ip_addr):
			if SYN_FLAG == packet.sprintf("%TCP.flags%"): # Is it a syn packet?

				if ip_addr in syn_counting_table.keys() and syn_counting_table[ip_addr][SIZE] > 0: # Check if we have seen this IP before
					size = syn_counting_table[ip_addr][SIZE] + 1

					while time_of_arrival - syn_counting_table[ip_addr][QUEUE][0] > TIME_INTERVAL:
						size -= 1
						heappop(syn_counting_table[ip_addr][QUEUE])

					if size >= MAX_SYNS_ALLOWED_IN_TIME_INTERVAL:
						# Block this ip address and flag it as such
						run = os.system('sudo iptables -A INPUT -s ' + str(ip_addr) + ' -j DROP')
						print('Blocking')
						syn_counting_table[ip_addr][BLOCKED] = True

					syn_counting_table[ip_addr][SIZE] = size # Regardless, update the count 
				else:
					# Add new IP address to the dictionary
					syn_counting_table[ip_addr] = {SIZE : 1, QUEUE: [time_of_arrival], BLOCKED : False}





def is_blocked(ip):
	if ip in syn_counting_table.keys():
		return syn_counting_table[ip][BLOCKED]
	else:
		# If this IP is not in our data structure it means it never sent a SYN packet to us
		# So it is not blocked
		return False


def main():
    sniff(prn=on_packet)


if __name__ == '__main__':
    main()
