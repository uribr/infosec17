import os


def error(message):
    print('\x1b[31m{}\x1b[0m'.format(message))


def check_if_nonempty(path):
    if not os.path.exists(path):
        error('ERROR: %s does not exist' % path)
        return False
    with open(path) as reader:
        data = reader.read().strip()
    if not data:
        error('ERROR: %s is empty' % path)
        return False
    return True


def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if all([
        check_if_nonempty('q1/q1a.py'),
        check_if_nonempty('q1/q1a.txt'),
        check_if_nonempty('q1/q1b.py'),
        check_if_nonempty('q1/q1b.txt'),
        check_if_nonempty('q1/q1c.txt'),
        check_if_nonempty('q1/q1d.py'),
        check_if_nonempty('q1/q1d.txt'),
        check_if_nonempty('q2/a/winston.py'),
        check_if_nonempty('q2/a/julia.py'),
        check_if_nonempty('q2/a/bigbrother.py'),
        check_if_nonempty('q2/a/q2a1.txt'),
        check_if_nonempty('q2/a/q2a2.txt'),
        check_if_nonempty('q2/b/winston.py'),
        check_if_nonempty('q2/b/julia.py'),
        check_if_nonempty('q2/b/bigbrother.py'),
        check_if_nonempty('q2/b/q2b1.txt'),
        check_if_nonempty('q2/b/q2b2.txt'),
    ]):
        print('smoketest seems cool')


if __name__ == '__main__':
    smoketest()
