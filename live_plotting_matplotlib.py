import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from collections import deque
import time

# import random
from numpy import random

import threading, socket, sys

HOST = "127.0.0.1"
PORT = 65432
conn = None
val = -1


def connection():
    global conn
    global res
    global val
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except Exception:
            print("Exception Error: Unable to Open Specified Port: " + str(PORT))
            return
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            # connect_button.pack_forget()
            #            conn.sendall(b"Welcome to Borealis Mission Control")
            # s.recv()
            while True:
                rec = conn.recv(1024).decode("utf-8")
                val = int(rec)
                if not rec:
                    conn.close()
                    sys.exit(1)


connection_thread = threading.Thread(target=connection, daemon=True)
connection_thread.start()

style.use("fivethirtyeight")

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax1.set_ylim([0, 100])

xdata = deque([i for i in range(20)], maxlen=20)
ydata = deque([0] * 20, maxlen=20)
(line,) = ax1.plot(xdata, ydata, lw=10)


def animate(i, ydata):
    ydata.append(val)
    line.set_ydata(ydata)
    return (line,)


ani = animation.FuncAnimation(fig, animate, fargs=(ydata,), interval=10, blit=True)
plt.show()
