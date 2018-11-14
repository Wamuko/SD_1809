from collections import deque
from datetime import datetime
import threading
import concurrent.futures as futures
import sys
import multiprocessing as mp
import time

if not __name__ == "__main__":
    import Sensor

BUFFER_MAX_LEN = 10000
RECV_BUFFER_SIZE = 1024

ProcessEnd = False
DEFAULT_FETCH_SPAN = 600
ECO_FETCH_SPAN = 7200


class SensorBuffer:
    def __init__(self):
        self.fetch_span = DEFAULT_FETCH_SPAN
        self.last_fetch_time = None
        self.__humidity = deque(maxlen=BUFFER_MAX_LEN)
        self.__luminosity = deque(maxlen=BUFFER_MAX_LEN)
        self.__listening_thread = None
        self.__parent_conn = None
        self.__lock = threading.Lock()

    def get_humidity(self):
        """ return None or int"""
        lock = self.__lock
        lock.acquire()
        ret = 0
        print(self.__humidity)
        if len(self.__humidity) > 0:
            ret = self.__humidity[-1][1]

        lock.release()
        return ret

    def get_luminosity(self):
        lock = self.__lock
        lock.acquire()
        ret = 0
        if len(self.__luminosity) > 0:
            ret = self.__luminosity[-1][1]

        lock.release()
        return ret

    def get_current_condition(self, fetch=True):
        if fetch:
            return self.get_humidity(), self.get_luminosity()
        else:
            return self.__fetch_data(datetime.now().timestamp())

    def start(self, loop_func):
        print("thread start")
        self.__parent_conn, child_conn = mp.Pipe()
        child_proc = mp.Process(target=loop_func, args=(child_conn, ))
        child_proc.start()

        th = self.__listening_thread = threading.Thread(target=self.__listening_loop)
        th.start()

    def __listening_loop(self):
        global ProcessEnd
        print("loop start")
        try:
            while True:
                timestamp = datetime.now().timestamp()
                if self.last_fetch_time is None or timestamp - self.last_fetch_time > self.fetch_span:
                    try:
                        self.__fetch_data(timestamp)
                        if ProcessEnd:
                            break

                    except Exception as ex:
                        print(str(ex), file=sys.stderr)

        except Exception as ex:
            print(ex, file=sys.stderr)

        print("close (when only debug)", file=sys.stderr)
        self.__parent_conn.send("quit")
        self.__parent_conn.close()

    def __fetch_data(self, fetch_time):
        conn = self.__parent_conn
        self.last_fetch_time = fetch_time
        print("send sig")
        conn.send(b"1")
        hum, lum = conn.recv()
        print("%d %d" % (hum, lum))

        lock = self.__lock
        lock.acquire()
        self.__humidity.append((fetch_time,hum))
        self.__luminosity.append((fetch_time, lum))
        lock.release()

        return hum, lum


if __name__ == "__main__":
    from debug import pseudo_sensor
    buf = SensorBuffer()
    buf.fetch_span = 1

    def producer():
        buf.start(pseudo_sensor.loop)

    with futures.ThreadPoolExecutor(max_workers=2) as executor:
        pr = executor.submit(producer)

        print("submit")

        time.sleep(7)

        ProcessEnd = True
