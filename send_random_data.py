import socket
import time
import random

HOST = "127.0.0.1"
PORT = 6543

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    a = {"tc": 0, "p1": 0, "p2": 0, "p3": 0}
    s.connect((HOST, PORT))
    while True:
        # a = str(random.randint(0, 100)).encode("utf-8")
        a["tc"] = "0" + str(random.randint(100, 200))
        a["p1"] = "0" + str(random.randint(200, 500))
        a["p2"] = "0" + str(random.randint(500, 700))
        a["p3"] = "0" + str(random.randint(700, 999))

        s.send(str(a).encode("utf-8"))
        time.sleep(0.001)
