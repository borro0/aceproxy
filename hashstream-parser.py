

import sys
import io

time_marker = 0x00

def main():
    reference = datalog(sys.argv[1])
    comparison = datalog(sys.argv[2])
    sync=0

    #We assume the reference contains all data contained in the comparison

    for hash in reference:
        try:
            if comparison.next() != hash:
                comparison.back()
                if sync > 10:
                        #if reference.position() > 205940 and reference.position() < 205955:
                        print("Lost sync at: ref:{} ({}) cmp:{} ({})  \n".format(reference.position(), reference.peek(),comparison.position(),  comparison.peek()))
                sync = 0
                continue
            else:
                #if reference.position() > 205500 and reference.position() < 206500:
                if reference.position() % 10000 == 0:
                        print("Synchronized: ref:{} cmp:{} sync:{} \n".format(reference.position(), comparison.position(),sync))
                #comparison.next()
                sync+=1
                comparison.set_datapoint_value(comparison.cur_timestamp - reference.cur_timestamp)
        except StopIteration:
            break

    print("finished\n")

    #print results
    #for val in comparison.delaydata:
    #    print((val,)



class datalog:
    fd = 0
    cur_timestamp = 0
    time_marker = b'\x00'

    starttime =0
    timelength = 0
    pos = 0
    cur_bw = 0;

    delaydata = []
    bandwidth = []

    def position(self):
        return self.pos

    def __init__(self, filename):
        self.fd = open(filename, 'rb',buffering=2*18)

        # self.starttime = int.frombytes(fd.read(4))
        # self.timelength = int.frombytes(fd.read(4))
        self.timelength = 10000
        self.cur_timestamp =self.starttime
        self.delaydata = [0]
        self.bandwidth = [0]



    def __iter__(self):
        return self

    def __next__(self):
        byte = self.fd.read(1);
        if byte == self.time_marker:
            self.cur_timestamp += 1
            self.bandwidth = self.bandwidth + [0]
            self.bandwidth[self.cur_timestamp] = self.cur_bw
            self.cur_bw = 0
            return self.__next__()
        if byte == b'' :
            raise StopIteration() 
        else:
            self.pos+=1
            self.cur_bw += 1
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
        self.pos-=1
        self.fd.seek(-1,1)

    def set_datapoint_value(self,val):
        self.delaydata = self.delaydata + [0]*(self.cur_timestamp - len(self.delaydata) +1)
        self.delaydata[self.cur_timestamp-self.starttime] = val


if __name__ == "__main__":
    main()