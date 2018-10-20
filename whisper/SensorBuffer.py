from queue import Queue

BUFFER_MAX_LEN = 10000


class SensorBuffer:
    def __init__(self):
        self.__humidity = Queue(BUFFER_MAX_LEN)

    def get_humidity(self):
        return 50

    def get_temperture(self):
        return 20

    def get_luminesity(self):
        return 700
