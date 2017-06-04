from scapy.all import *
import math

SYN = 'S'
ACK = 'A'
BIT_IN_BYTE = 8
NUMBER_OF_OPTION_BITS = 3
MASK = 7

next_seq = 0
number_of_packets = -1
data = []


def is_last_packet(packet):
	global number_of_packets

	# check if this is the last packet using the seq number and the ack number
	if packet != None and packet.haslayer(TCP):
		handler(packet)
		tcp = packet.getlayer(TCP)
		if tcp.seq == tcp.ack - 1 and tcp.seq == number_of_packets:
			return True
	return False

def handler(packet):
	global next_seq
	global number_of_packets
	global data

	tcp = packet.getlayer(TCP)
	# Ignore any retransmissions (Kinda useless because we checked for it in the filter but it's harmless and it works so I'll just leave it here)
	if tcp.seq >= next_seq:
		# Use the first packet to determine how many packets are going to be send (the ack field holds that number)
		if number_of_packets == -1:
			number_of_packets = tcp.ack - 1
			data = [0] * tcp.ack
		next_seq += 1

		# Pad with zeroes to match 3 bits if needed
		temp = bin(tcp.reserved & MASK)[2:]
		padding_length = 3 - len(temp)
		data[tcp.seq] = '0' *  padding_length + temp

def filter(packet):
	global next_seq


	if packet != None and packet.haslayer(TCP):
		# verify the senders' IP
		if packet.getlayer(IP).dst == '127.0.0.1':
			tcp = packet.getlayer(TCP)
			# Verify source and destination ports
			if tcp.dport == 1984 and tcp.sport == 65000:
				flags = tcp.sprintf('%TCP.flags%')
				# Verify the type of the tcp packet
				if SYN in flags and ACK in flags:
					# verify that this is the next packet we are expecting
					if tcp.seq == next_seq:
						return True
	return False

def receive_message(port):
	global string
	sniff(lfilter = filter, stop_filter = is_last_packet)
	# Some data manipulation (we sent it from LSB to MSB and built it the same way so we now need to invert the direction)
	data.reverse() 
	string = ''
	binary_string = string.join(data) 
	# Get the offset needed (because we padded it to be a multiple of 3 and now we want to look at block of 8 bits)
	offset = len(binary_string) % 8 
	# Get the length (each byte it 8 bits because Winston padded all the bytes to be 8 bit long before sending)
	string_length = len(binary_string)/8
	# Finally, reconstruct the string
	for i in range(string_length):
		string += chr(int(binary_string[offset + i * BIT_IN_BYTE : offset + (i + 1) * BIT_IN_BYTE], 2))
	return string

def main():
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()
