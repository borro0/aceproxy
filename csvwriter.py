import time
from multiprocessing import Event
from Queue import Empty

stop_command = Event()


class CSVWriter(object):

    def __init__(self, filename):
        # Append current date and time to filename
        self.filename = filename + time.strftime("%Y%m%d-%H%M%S")

    def writer(self, queue):
        with open(self.filename, 'w+') as f:
            while not queue.empty() or not stop_command.is_set():
                try:
                    data = queue.get_nowait()
                    hashed_data = self.hash_data(data)
                    # Floating point of time since epoch in seconds
                    ts = time.time()
                    f.write("{0}|{1},".format(str(hashed_data), ts))

                except Empty:
                    # This should never happen
                    pass

    def hash_data(self, packet):
        # TODO Hash the packet with some hash function
        return packet

    def stop(self):
        global stop_command
        stop_command.set()
