import time
import serial
import os

REPEAT = range(5)
DISCARD = range(20)

DEFAULT_HUMIDITY = 700
DEFAULT_LUMINOSITY = 50

ser = serial.Serial("/dev/ttyUSB_whisper", 9600)
print(ser)


def debug_main():
    while 1:
        time.sleep(1)
        sig = ("A" + os.linesep).encode()
        print("write %s" % sig)

        ser.write(sig)

        print(try_read())


def loop(conn):
    time.sleep(2)
    while 1:
        msg = conn.recv()
        print("Sensor: msg = %s" % msg)
        if msg == "quit":
            conn.close()
            break
        else:
            conn.send(try_read())


def try_read():
    hum = lum = -1
    for i in range(5):
        ser.write(("A" + os.linesep).encode())
        print("read")
        # hum_histgram = {}
        # lum_histgram = {}
        byte_seq = ser.readline()
        hum, lum = map(int, byte_seq.decode().split())
        if hum != -1 and lum != -1:
            return (hum, lum)

    return DEFAULT_HUMIDITY, DEFAULT_LUMINOSITY
    # for _ in REPEAT:
    #     hum, lum = map(int, ser.readline().decode().split())
    #     for _ in DISCARD:
    #         ser.readline()

    #     if hum in hum_histgram:
    #         hum_histgram[hum] = 0
    #     else:
    #         hum_histgram[hum] += 1

    #     if lum in lum_histgram:
    #         lum_histgram[lum] = 0
    #     else:
    #         lum_histgram[lum] += 1

    # return (max(hum_histgram, key=hum_histgram.get),
    #         max(lum_histgram, key=lum_histgram.get))


if __name__ == "__main__":
    time.sleep(3)
    debug_main()
