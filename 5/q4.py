import os, sys

import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'


def get_string(student_id):
    return 'Take me (%s) to your leader!' % student_id


def get_arg():
    raise NotImplementedError()


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)
