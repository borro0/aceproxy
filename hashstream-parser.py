

import sys
import io
import fcntl

time_marker = 0x00

def main():
    reference = datalog(sys.argv[1])
    comparison = datalog(sys.argv[2])

    #We assume the reference contains all data contained in the comparison
    for hash in reference:
        try:
            if comparison.next() != hash:
                comparison.back()

                if reference.position() % 100000 == 0:
                        print("No Match found at: ref:{} cmp:{} \n".format(reference.position(), comparison.position()))
                continue
            else:
                if reference.position() % 10000 == 0:
                        print("Match found at: ref:{} cmp:{} \n".format(reference.position(), comparison.position()))
                #comparison.next()
                comparison.set_datapoint_value(comparison.cur_timestamp - reference.cur_timestamp)
        except StopIteration:
            break

    print("finished\n")

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

    def position(self):
        return self.fd.tell()

    def __init__(self, filename):
        self.fd = open(filename, 'rb',buffering=2*18)

        fd = self.fd.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        # self.starttime = int.frombytes(fd.read(4))
        # self.timelength = int.frombytes(fd.read(4))
        self.timelength = 10000
        self.cur_timestamp =self.starttime
        self.datapoints = [0]*self.timelength

    def __iter__(self):
        return self

    def __next__(self):
        byte = self.fd.read(1);
        if byte == self.time_marker:
            self.cur_timestamp += 1
            return self.__next__()
        if byte == '' :
            raise StopIteration() 
        else:
            return byte


    def next(self):
        return self.__next__()

    def peek(self):
        #return self.fd.peek(1)
        byte = self.fd.read(1)
        if byte == '':
            raise StopIteration()
        self.fd.seek(-1,1)
        return byte

    def back(self):
        self.fd.seek(-1,1)

    def set_datapoint_value(self,val):
        self.datapoints[self.cur_timestamp-self.starttime] = val


if __name__ == "__main__":
    main()