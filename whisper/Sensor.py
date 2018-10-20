from socket import socket, AF_INET, SOCK_STREAM
import time
import serial

HOST = "localhost"
PORT = 51000

REPEAT = range(5)


def read_mode():
    histgram = {}
    for i in REPEAT:
        val = int(ser.readline())
        if val in histgram:
            histgram[val] = 0
        else:
            histgram[val] += 1
    max_v = max(histgram.values())
    return histgram[max_v]


if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_STREAM)
    ser = serial.Serial("/dev/ttyACM0", 9600)
    time.sleep(3)
    data = []
    histgram = {}
    while 1:
        conn, addr = sock.accept()
        # block
        conn.recv(8)
        ser.write((1).to_bytes(1, "big"))
        time.sleep(0.2)

        # read humidity and luminosity
        hum = read_mode()
        lum = read_mode()

        # send data
        sock.connect((HOST, PORT))
        data = ("%d %d" % (hum, lum)).encode()
        sock.send(data)
