from socket import socket, AF_INET, SOCK_STREAM
import time
import serial

HOST = "localhost"
PORT = 51000

REPEAT = range(5)
DISCARD = range(20)


def read_mode():
    hum_histgram = {}
    lum_histgram = {}
    for i in REPEAT:
        hum, lum = map(int, ser.readline().decode().split())
        for _ in DISCARD:
            ser.readline()

        if hum in hum_histgram:
            hum_histgram[hum] = 0
        else:
            hum_histgram[hum] += 1

        if lum in lum_histgram:
            lum_histgram[lum] = 0
        else:
            lum_histgram[lum] += 1

    return (max(hum_histgram, key=hum_histgram.get),
            max(lum_histgram, key=lum_histgram.get))


if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((HOST, PORT))

    ser = serial.Serial("/dev/ttyACM0", 9600)

    time.sleep(3)

    while 1:
        sock.recv(8)
        ser.write((1).to_bytes(1, "big"))

        # read humidity and luminosity
        hum, lum = read_mode()

        # send data
        data = ("%d %d" % (hum, lum)).encode()
        sock.send(data)
