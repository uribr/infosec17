from scapy.all import *


def stealth_syn_scan(ip, ports, timeout):
    # The list to be returned
    statuses = []
    for port in ports:
        # The Stealth-O-Packet
        cyber_ninja_packet = IP(dst = ip) / TCP(dport = port, flags = 'S')

        # Infiltrating the Palace
        response = sr1(cyber_ninja_packet, timeout = timeout, verbose = False)
      
        # No answer means this port is being filtered
        if response == None:
            statuses += ['filtered']
            continue
        # Get the flags
        else :
        	tcp_response_flags = response.sprintf("%TCP.flags%")    

        if 'S' in tcp_response_flags and 'A' in tcp_response_flags:
            statuses += ['open']
            send(IP(dst = ip) / TCP(dport = port, flags = 'RA'), verbose = False)
        elif 'R' in tcp_response_flags:
            statuses += ['closed']
        else: 
            statuses += ['filtered']

    return statuses


def main(argv):
    if not 3 <= len(argv) <= 4:
        print('USAGE: %s <ip> <ports> [timeout]' % argv[0])
        return 1
    ip    = argv[1]
    ports = [int(port) for port in argv[2].split(',')]
    if len(argv) == 4:
        timeout = int(argv[3])
    else:
        timeout = 5
    results = stealth_syn_scan(ip, ports, timeout)
    for port, result in zip(ports, results):
        print('port %d is %s' % (port, result))


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
