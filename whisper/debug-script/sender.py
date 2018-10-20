from socket import socket, AF_INET, SOCK_STREAM
import time

HOST = "localhost"
PORT = 51000


def send(byte_seq):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.send(byte_seq)


if __name__ == "__main__":
    n = 150
    while True:
        try:
            text = "%d %d %d" % (n, n, n)
            send(text.encode())
            print("send %d" % n)
            if n == 0:
                break
            n -= 1
            time.sleep(0.6)
        except Exception as ex:
            print(str(ex))
            break

    print("connection end")
