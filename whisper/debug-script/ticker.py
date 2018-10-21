from socket import socket, AF_INET, SOCK_STREAM
import time
import datetime
import concurrent.futures as futures

HOST = "localhost"
PORT = 51000

# server
sock = socket(AF_INET, SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(2)

conn, addr = sock.accept()

while True:
    time.sleep(1)
    print("awake")
    # tick
    try:
        conn.send(b"1")
    except Exception as ex:
        print(ex)
        continue

    byte_seq = conn.recv(4000)
    print(byte_seq.decode())