from scapy.all import *
from time import *
from heapq import *
from subprocess import Popen

SIZE = 'queue-size'
BLOCKED = 'is-blocked'
QUEUE = 'minimum-heap'
PASSWORD = 1234
SYN_FLAG = 'S'
MAX_SYNS_ALLOWED_IN_TIME_INTERVAL = 15
TIME_INTERVAL = 60
syn_counting_table = dict()


def on_packet(packet):
	time_of_arrival = time()
	ip_addr = packet.getlayer(IP).src
	if pakcet != None:
		if SYN_FLAG in packet.sprint("%TCP.flags"):
			if ip_addr in syn_counting_table:

				size = syn_counting_table[ip_addr][SIZE] + 1

				while time_of_arrival - syn_counting_table[ip_addr][QUEUE][0] > TIME_INTERVAL:
					size -= 1
					syn_counting_table[ip_addr][QUEUE].heappop()

				if size >= MAX_SYNS_ALLOWED_IN_TIME_INTERVAL:
					# Block this ip address
					run = Popen(['sudo iptables -I INPUT -s ' + str(ip_addr), PASSWORD])

					syn_counting_table[ip_addr][SIZE] = size
					syn_counting_table[ip_addr][BLOCKED] = True


			else:
				syn_counting_table[ip] = {SIZE : 1, QUEUE: heapify([time_of_arrival]), BLOCKED = False}




def is_blocked(ip):
    return syn_counting_table[ip][BLOCKED]


def main():
    sniff(prn=on_packet)


if __name__ == '__main__':
    main()
