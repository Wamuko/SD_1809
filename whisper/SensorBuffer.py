from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM
import sys

HOST = "localhost"
PORT = 51000
NUM_THREAD = 2
BUFFER_MAX_LEN = 10000
RECV_BUFFER_SIZE = 1024


class SensorBuffer:
    def __init__(self):
        self.__humidity = Queue(BUFFER_MAX_LEN)
        self.__temperture = Queue(BUFFER_MAX_LEN)
        self.__luminosity = Queue(BUFFER_MAX_LEN)
        sock = self.__sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(NUM_THREAD)

    def get_humidity(self):
        return 50

    def get_temperture(self):
        return 20

    def get_luminosity(self):
        return 700

    def start(self):
        while True:
            try:
                conn, addr = sock.accept()
                byte_seq = conn.recv(RECV_BUFFER_SIZE)
                hum, tmp, lum = byte_seq.decode()
                __push_buffer(self.__humidity, hum)
                __push_buffer(self.__temperture, tmp)
                __push_buffer(self.__luminosity, lum)

            except UnicodeDecodeError as err:
                continue

            except Exception as ex:
                print(str(ex), file=sys.stderr)

    @staticmethod
    def __push_buffer(buffer, data):
        if buffer.full():
            buffer.get()

        buffer.put(data)
