from scapy.all import *


def receive_message(port):
    pass # Reimplement me! (b2)


def main():
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()
