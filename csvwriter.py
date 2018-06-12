import time
from multiprocessing import Event
from Queue import Empty
import hashlib
from apscheduler.schedulers.background import BackgroundScheduler
import logging

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
        with open(self.filename, 'wb+') as f:
            f.write(int(time.time()*10).to_bytes(8,byteorder='big'))
            while not queue.empty() or not stop_command.is_set():
                try:
                    data = queue.get_nowait()
                    if len(data) < 6 and data == "$101$":
                        f.write(b'\x00')
                    else:
                        hashed_data = self.hash_data(data)
                        # Floating point of time since epoch in seconds
                        # f.write("{0}|{1}\n,".format(str(hashed_data), ts))

                        f.write(hashed_data[0] if hashed_data[0] != 0 else 1)
                except Empty:
                    # This should never happen
                    pass
            f.flush()
        sched.shutdown()

    def hash_data(self, packet):
        hash_object = hashlib.sha1(packet)
        hex_dig = hash_object.digest()
        return hex_dig

    def stop(self):
        global stop_command
        stop_command.set()

    def insert_marker(self, queue):
        queue.put("$101$")
