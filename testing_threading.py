import threading, socket, sys
import tkinter as tk
import time
import json
import asyncio
import re

HOST = "172.20.10.10"
PORT = 65432
conn = None
LENGTH_OF_RECV = 24
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
            # HEADERSIZE = 0
            # while True:
            #     full_msg = ""
            #     new_msg = True
            #     while True:
            #         msg = conn.recv(16)
            #         if new_msg:
            #             print("new msg len:", msg[:HEADERSIZE])
            #             msglen = int(msg[:HEADERSIZE])
            #             new_msg = False

            #         print(f"full message length: {msglen}")

            #         full_msg += msg.decode("utf-8")

            #         print(len(full_msg))

            #         if len(full_msg) - HEADERSIZE == msglen:
            #             print("full msg recvd")
            #             print(full_msg[HEADERSIZE:])
            #             new_msg = True
            #             full_msg = ""

            while True:

                time.sleep(0.001)
                resp = conn.recv(LENGTH_OF_RECV)
                # res.set(resp2["val"])
                get_refined_data(resp)
                if not resp:
                    conn.close()
                    sys.exit(1)


def get_refined_data(new_data):
    global old_resp
    data = re.search("{*}", old_resp + new_data)
    val = json.loads(data)
    print(val["val"])
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
    connect_button.pack()


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
