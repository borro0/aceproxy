

# Custom Scripts
from csvwriter import CSVWriter
import requests
import sys
from collections import deque
from multiprocessing import Process, Queue
class parser:


    requestlist = []
    byte_counter = 0
    current_packet_list = [None]*188
    in_sync = False

    def send_packet(self):
        packet = b''.join(self.current_packet_list)
        writer_q.put(packet)
        self.byte_counter = 0

    def parse_data(self, data_chunk):
        # possible states: search for sync byte, in_sync
        #logger.debug("Reading a new data_chunk")        
        for byte in data_chunk:
            self.byte_counter += 1
            # logger.debug(hex(ord(byte)))
            if byte == 'G':
                if self.byte_counter == 188:
                    if not self.in_sync:
                        logger.debug("We are in sync now")
                        self.in_sync = True
                    #logger.debug("Sync byte found after %i, resetting counter" % self.byte_counter)
                    else
                        self.send_packet()

                elif self.byte_counter > 188:
                    if not self.in_sync:
                        logger.debug("Not in sync yet, sync byte found after %i, resetting counter" % self.byte_counter)
                        self.byte_counter = 0
                    else:
                        logger.error("We received a longer byte than expected: %i" % self.byte_counter)
                        self.send_packet()

                # Check the current packet list does not get too long
                if len(self.current_packet_list) > 1000:
                    logger.debug("Lise size is over 1000, something is wrong")
                    del self.current_packet_list[:]

                # Append our new byte to the current list packet
                if self.in_sync:
                    self.current_packet_list[self.byte_counter] = byte
            else:
                self.current_packet_list[self.byte_counter] = byte


if __name__ == '__main__':
    #freeze_support()
    # Custom output data inits #############
    # TODO Take filename from kwargs
    output_filename = sys.argv[2] if len(sys.argv) >= 2 else "OUTPUT"
    writer_q = Queue()
    csv_w = CSVWriter(output_filename, writer_q)
    w_process = Process(target=csv_w.writer, args=(writer_q,))
    w_process.start()
    print("Writer started with pid {0}, filename: {1}".format(w_process.pid, output_filename))
    p = parser()

    r = requests.get(sys.argv[1],stream=True)
    for chunk in r.iter_content(chunk_size=1024):
        p.parse_data(chunk)