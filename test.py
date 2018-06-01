import time
from csvwriter import CSVWriter
from multiprocessing import Process, Queue

if __name__ == '__main__':
    q = Queue()
    cw = CSVWriter("TEST")

    p = Process(target=cw.writer, args=(q,))
    p.start()
    try:
        while True:
            q.put("TestTest")
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    p.join()

