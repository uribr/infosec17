from subprocess import Popen
from time import sleep
import json

def generate_valid_script():
	return json.dumps({"command": "echo cool", "signature": "6c68e3c88a87339fa8667cb36c82d4cf0bdcc131efcf98eb8df1867122e66e0e2e9d8d1ce01c40261fb8bde61a7768215c20febc2cd522af3a2232be73cabe3ada6d86b1635a52c787bd7d97985f4ce2ef9b47ea0c72bdb35b702f9169218adc2d4cd53eabfc3c875bef05270b703d407afb5b22198d56f3489ec8e3241c19a9"})

def generate_invalid_script():
	return json.dumps({"command" : "echo hacked", "signature" : "BOOP"})

def write_script(script):
	with open('foo', 'w') as writer:
		writer.write(script)
		writer.truncate()

def main():
	# First, get a command with a valid signature.
	script = generate_valid_script()

	# Next we write it to a file and call run.py with it
	write_script(script)
	run = Popen(['python', 'run.py', 'foo'])
	sleep(0.5)
	# The validation takes a couple of precious seconds.
	# In that time we get a new script that only holds a commnad.
	script = generate_invalid_script()
	# Then we overwrite the file we passed to run.py.
	write_script(script)
	# Because the execution method reopens the file to read it
	# it will open the new file we just wrote, the one with no signature.

	# All thats left is to Wait for success... any second now...
	run.wait()

if __name__ == '__main__':
	main()