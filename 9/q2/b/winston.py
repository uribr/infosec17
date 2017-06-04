from scapy.all import *


SYN = 'S'
ACK = 'A'
BIT_IN_BYTE = 8
NUMBER_OF_OPTION_BITS = 3
MASK = 7
SOURCE_PORT = 65000
plaintext = 'I love you'


def send_message(ip, port):
	# Get the bytes
	bytes_array = [bytearray(plaintext)[i] for i in range(len(plaintext))]

	# Get 8-bit (with sign-extension if needed) of each byte
	binary_array = [format(bytes_array[i], '08b') for i in range(len(plaintext))]

	# Concatenate all the 8-bit representations to one string
	binary_string = ''.join(binary_array[i] for i in range(len(plaintext)))

	# Pad the string to be a multiple of 3 so as to fill the entirety of the space available for sending data in the reserved field of a tcp header
	binary_string = '0' * (NUMBER_OF_OPTION_BITS - len(plaintext) % NUMBER_OF_OPTION_BITS) + binary_string

	# Treat the string as base-2 number
	all_data = int(binary_string, 2)
	ack = len(binary_string) / 3

	ip_layer = IP(dst = ip)

	for seq in range(ack):
		# Take 3 LSBs 
		data = all_data & MASK

		tcp_layer = TCP(dport = port, sport = SOURCE_PORT, seq = seq, ack = ack, reserved = data, flags = SYN + ACK)
		packet = ip_layer / tcp_layer
		send(packet, verbose = False)

		# Shift 3 bits to the right to get the next 3 bits
		all_data >>= NUMBER_OF_OPTION_BITS






def main():
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()
