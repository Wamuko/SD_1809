from collections import deque
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
import threading
import concurrent.futures as futures
import sys
import time

HOST = "localhost"
PORT = 51000
NUM_THREAD = 2
BUFFER_MAX_LEN = 10000
RECV_BUFFER_SIZE = 1024

ProcessEnd = False
DEFAULT_FETCH_SPAN = 600


class SensorBuffer:
    def __init__(self):
        self.fetch_span = DEFAULT_FETCH_SPAN
        self.last_fetch_time = None
        self.__humidity = deque(maxlen=BUFFER_MAX_LEN)
        self.__luminosity = deque(maxlen=BUFFER_MAX_LEN)
        self.__sock = socket(AF_INET, SOCK_STREAM)

    def get_humidity(self):
        """ return None or int"""
        lock = threading.Lock()
        lock.acquire()
        ret = 0
        if len(self.__humidity) > 0:
            ret = self.__humidity[-1]

        lock.release()
        return ret

    def get_luminosity(self):
        lock = threading.Lock()
        lock.acquire()
        ret = 0
        if len(self.__luminosity) > 0:
            ret = self.__luminosity[-1]

        lock.release()
        return ret

    def start(self):
        self.last_fetch_time = datetime.now()
        sock = self.__sock
        sock.bind((HOST, PORT))
        sock.listen(NUM_THREAD)
        conn, addr = sock.accept()
        push = SensorBuffer.__push_data
        print("start")
        global ProcessEnd
        while True:
            unix_time_now = datetime.now().strftime('%s')
            unix_time_last_fetch = self.last_fetch_time.strftime('%s')
            if unix_time_now - unix_time_last_fetch > self.fetch_span:
                try:
                    byte_seq = conn.recv(RECV_BUFFER_SIZE)
                    hum, lum = map(int, byte_seq.decode().split())
                    push(self.__lock, self.__humidity, hum)
                    push(self.__lock, self.__luminosity, lum)
                    if ProcessEnd:
                        break
                except UnicodeDecodeError:
                    continue

                except Exception as ex:
                    print(str(ex), file=sys.stderr)

        print("close (when only debug)", file=sys.stderr)
        sock.close()

    @staticmethod
    def __push_data(lock, buffer, data):
        lock.acquire()
        buffer.append(data)
        lock.release()


if __name__ == "__main__":
    buf = SensorBuffer()

    def producer():
        buf.start()

    def consumer():
        cnt = 0
        print("consumer starts")
        while cnt < 10:
            time.sleep(1)
            h = buf.get_humidity()
            if h is not None:
                print("hum = %d" % h)
                cnt += 1

    with futures.ThreadPoolExecutor(max_workers=2) as executor:
        pr = executor.submit(producer)
        cs = executor.submit(consumer)
        while cs.running():
            pass

        print("cs end", file=sys.stderr)
        ProcessEnd = True
