import threading
import socket
import sys
import tkinter as tk
import time
import json
import re

HOST = "10.0.0.2"
PORT = 65432
conn = None
LENGTH_OF_RECV = 49
resp = b""
old_resp = b""


def connection():
    global conn
    global resp
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
            connected()
            while True:

                time.sleep(0.001)
                resp = conn.recv(LENGTH_OF_RECV)
                get_refined_data(resp)
                if not resp:
                    conn.close()
                    sys.exit(1)


def get_refined_data(new_data):
    global old_resp
    # print(old_resp.decode("utf=8") + new_data.decode("utf-8"))
    data = re.findall("\{(.*?)\}", old_resp.decode("utf=8") + new_data.decode("utf-8"))
    # print(data)
    if data:
        val = json.loads("{" + data[0] + "}")
        # textValue.set(val["val"], end=" ")
        print(f"tc: {val['tc']}", end=" ")
        print(f"p1: {val['p1']}", end=" ")
        print(f"p2: {val['p2']}", end=" ")
        print(f"p3: {val['p3']}", end=" ")
        print()
    old_resp = new_data


def connect():
    connection_thread = threading.Thread(target=connection, daemon=True)
    connection_thread.start()


def connected():
    button.pack()
    button2.pack()
    text.pack()
    quit_button.pack()
    win.title("Connected to BOREALIS")
    connect_button.pack_forget()


def disconnect():
    conn.send(b"quit")
    conn.close()
    sys.exit(1)


win = tk.Tk()
HEIGHT = 600
WIDTH = 480
win.title("MACH")
win.geometry(f"{HEIGHT}x{WIDTH}")
button = tk.Button(text="Open Valves", command=lambda: conn.send(b"open"))
button2 = tk.Button(text="Close Valves", command=lambda: conn.send(b"close"))
textValue = tk.StringVar()
connect_button = tk.Button(text="CONNECT TO BOREALIS", command=connect)
quit_button = tk.Button(text="Disconnect", command=disconnect)

text = tk.Label(textvariable=textValue)
connect_button.pack()

win.mainloop()
