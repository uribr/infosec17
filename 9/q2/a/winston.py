import socket
import os
from Crypto.Cipher import AES

key = b'Valar Morghulis!'
LOVE = 'I love you'
def send_message(ip, port):
	iv = os.urandom(len(key))
	cipher = AES.new(key, AES.MODE_CBC, iv)
	padding_length = 16 - (len(LOVE + '\0') % 16)
	plaintext = LOVE + '\0' + chr(padding_length) * padding_length
	msg = iv + cipher.encrypt(plaintext)
	
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
