import socket
from Crypto import *

key = b'Valar Morghulis!'
LOVE = 'I love you'
def send_message(ip, port):
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	padding_length = 16 - (len(data) % 16)
	plaintext = LOVE + chr(padding_length) * padding_length
	msg = iv + ciper.encrypt(plaintext)
	
    # Reimplement me! (b1)
    connection = socket.socket()
    try:
        connection.connect((ip, port))
        connection.send(msg)
    finally:
        connection.close()


def main():
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()
