import socket
import time
import random
import json

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    a = {"p1": 0, "p2": 0, "p3": 0}
    s.connect((HOST, PORT))
    while True:
        # a = str(random.randint(0, 100)).encode("utf-8")
        # a["tc"] = "0" + str(random.randint(100, 200))
        a["p1"] = "0" + str(random.randint(200, 500))
        a["p2"] = "0" + str(random.randint(500, 700))
        a["p3"] = "0" + str(random.randint(700, 999))

        s.send(json.dumps(a).encode("utf-8"))
        # if s.recv(1024).decode("utf-8") == "quit":
        #     s.close()
        #     exit()
        time.sleep(0.05)
