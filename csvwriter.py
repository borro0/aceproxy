import time
from multiprocessing import Event
from Queue import Empty
import hashlib
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import xxhash
import uptime

logging.getLogger('apscheduler.scheduler').setLevel('WARNING')
logging.getLogger('apscheduler.executors.default').setLevel('WARNING')

sched = BackgroundScheduler()
stop_command = Event()


class CSVWriter(object):

    def __init__(self, filename, queue):
        # Append current date and time to filename
        self.filename = "{0}-{1}.bin".format(filename,
                                             time.strftime("%Y%m%d-%H%M%S"))
        sched.add_job(self.insert_marker, 'interval', args=[queue], seconds=0.1)
        sched.start()

    def writer(self, queue):
        with open(self.filename, 'wb+',1024) as f:
            n = int(time.time()*1000)
            f.write(self.to_bytes(n,8,endianess='big'))
            packet_counter = 0
            while not stop_command.is_set():
                try:
                    data = queue.get(True,1)
                    if len(data) < 6 and data == b'$101$':
                        f.write(b'\x00')

                        n = int(time.time()*1000)
                        f.write(self.to_bytes(n,8,endianess='big'))
                        print(n)

                    else:
                        hashed_data = self.hash_data(data)
                        packet_counter += 1
                        
                        # write time marker every 240 packets
                        if packet_counter >= 240:
                            f.write(b'\x00')
                            n = int(time.time()*1000)
                            f.write(self.to_bytes(n,8,endianess='big'))
                            packet_counter = 0

                        # Floating point of time since epoch in seconds
                        # f.write("{0}|{1}\n,".format(str(hashed_data), ts))

                        f.write(hashed_data if hashed_data != b'\x00' else b'\x01')
                except Empty:
                    # This should never happen
                    pass
            f.flush()
        sched.shutdown()

    def hash_data(self, packet):
        hash_object = xxhash.xxh32(packet)
        return hash_object.digest()[0]
        

    def stop(self):
        global stop_command
        stop_command.set()

    def insert_marker(self, queue):
        queue.put(b'$101$')

    def to_bytes(self, n, length, endianess='big'):
        h = '%x' % n
        s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
        return s if endianess == 'big' else s[::-1]
