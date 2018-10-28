import time
import serial

REPEAT = range(5)
DISCARD = range(20)

try:
    ser = serial.Serial("/dev/ttyACM0", 9600)
except Exception as ex:
    pass


def debug_main():
    while 1:
        time.sleep(1)
        print("read")
        ser.write("0".encode())

        print(read())


def loop(conn):
    while 1:
        msg = conn.recv()
        if msg == "quit":
            conn.close()
            break
        else:
            ser.write("0".encode())
            conn.send(read())


def read():
    # hum_histgram = {}
    # lum_histgram = {}
    hum, lum = map(int, ser.readline().decode().split())
    return (hum, lum)
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
    debug_main()
