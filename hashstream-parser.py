

import sys

time_marker = 0x00

def main():
	reference = datalog(sys.argv[1])
	comparison = datalog(sys.argv[2])

	#We assume the reference contains all data contained in the comparison
	for hash in reference:
		try:
			if comparison.peek() != hash:
				continue
			else
				comparison.next()
				comparison.set_datapoint_value(comparison.cur_timestamp - reference.cur_timestamp)
		except StopIteration:
			break

	#print results
	for val in comparison.datapoints:
		print(val)



class datalog:
	fd = 0
	cur_timestamp = 0
	time_marker = 0x00

	starttime =0
	timelength = 0

	datapoints = []

	def __init__(self, filename):
		self.fd = open(filename, 'rb')
		self.starttime = int.frombytes(fd.read(4))
		self.timelength = int.frombytes(fd.read(4))
		self.cur_timestamp =self.starttime
		self.datpaoints = [0]*self.timelength

	def __iter__(self):
		return self

	def next(self):
		byte = self.fd.read(1);
		if byte == self.time_marker:
			self.cur_timestamp += 1
			return self.next()
		if byte == '' :
			raise StopIteration() 
		else
			return byte

	def peek(self):
		byte = self.fd.read(1)
		self.fd.seek(-1)
		return byte

	def set_datapoint_value(val):
		self.datapoints[cur_timestamp-starttime] = val


if __name__ == "__main__":
    main()