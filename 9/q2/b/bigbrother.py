from scapy.all import *


unpersons = set()


def spy(packet):
    pass # Reimplement me! (b1)


def main():
    sniff(prn=spy)


if __name__ == '__main__':
    main()