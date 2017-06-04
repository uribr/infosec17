import socket
import os
from Crypto.Cipher import AES


key = b'Valar Morghulis!'
def receive_message(port):
	listener = socket.socket()
	try:
		listener.bind(('', port))
		listener.listen(1)
		connection, address = listener.accept()
		try:
			ciphertext = connection.recv(1024)
			iv = ciphertext[:16]
			cipher = AES.new(key, AES.MODE_CBC, iv)
			plaintext = (cipher.decrypt(ciphertext[16:]))

			return plaintext
		finally:
			connection.close()
	finally:
		listener.close()


def main():
	message = receive_message(1984)
	print('received: %s' % message)


if __name__ == '__main__':
	main()
