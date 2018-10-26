# from socket import socket, AF_INET, SOCK_STREAM
# from ..port_setting import HOST, PORT
import sys

# HOST = "localhost"
# PORT = 51000

# sock = socket(AF_INET, SOCK_STREAM)
# sock.connect((HOST, PORT))

# while 1:
#     sock.recv(8)

#     data = ("%d %d" % (hum, lum))
#     print(data, file=sys.stderr)
#     sock.send(data.encode())
#     hum += 1
#     lum += 1


def loop(conn):
    hum = 100
    lum = 109
    print("start sensor")
    try:
        while 1:
            msg = conn.recv()
            if msg == "quit":
                conn.close()
                break
            else:
                # ser.write((1).to_bytes(1, "big"))
                conn.send((hum, lum))
                hum += 1
                lum += 1
    except Exception as ex:
        print("from sensor")
        print(ex)

    print("pseudo-sensor.end")
    conn.close()
