import socket
import time
import random

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        a = str(random.randint(0, 100)).encode("utf-8")
        s.send(a)
        time.sleep(0.001)
