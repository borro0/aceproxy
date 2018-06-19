

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
        #delaydata("Reading a new data_chunk")        
        for byte in data_chunk:
            # print(hex(ord(byte)))
            self.byte_counter += 1
            if byte == 'G':
                if self.byte_counter == 188:
                    if not self.in_sync:
                        print("We are in sync now")
                        self.in_sync = True
                    #print("Sync byte found after %i, resetting counter" % self.byte_counter)
                    else:
                        self.send_packet()

                elif self.byte_counter > 188:
                    if not self.in_sync:
                        print("Not in sync yet, sync byte found after %i, resetting counter" % self.byte_counter)
                        self.byte_counter = 0
                    else:
                        print("We received a longer byte than expected: %i" % self.byte_counter)
                        self.send_packet()

                # Append our new byte to the current list packet
                if self.in_sync and self.byte_counter <= 188:
                    self.current_packet_list[self.byte_counter-1] = byte
            else:
                if(self.byte_counter <= 188):
                    self.current_packet_list[self.byte_counter-1] = byte


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