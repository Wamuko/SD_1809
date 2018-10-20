from socket import socket, AF_INET, SOCK_STREAM
import time
import serial

HOST = "localhost"
PORT = 51000

if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_STREAM)
    ser = serial.Serial("/dev/ttyACM0", 9600)
    time.sleep(3)
    while 1:
        data = seq.readline()
        sock.connect((HOST, PORT))
        sock.send(data)
