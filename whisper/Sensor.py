import time
import serial

REPEAT = range(5)
DISCARD = range(20)

ser = serial.Serial("/dev/ttyUSB0", 9600)


def debug_main():
    while 1:
        time.sleep(1)
        ser.write((1).to_bytes(1, "big"))

        print(read_mode())


def loop(conn):
    while 1:
        msg = conn.recv()
        if msg == "quit":
            conn.close()
            break
        else:
            ser.write((1).to_bytes(1, "big"))
            conn.send(read_mode())


def read_mode():
    hum_histgram = {}
    lum_histgram = {}
    for _ in REPEAT:
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
    debug_main()
