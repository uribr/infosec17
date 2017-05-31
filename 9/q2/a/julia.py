import socket


def receive_message(port):
    # Reimplement me! (a2)
    listener = socket.socket()
    try:
        listener.bind(('', port))
        listener.listen(1)
        connection, address = listener.accept()
        try:
            return connection.recv(1024)
        finally:
            connection.close()
    finally:
        listener.close()


def main():
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()
