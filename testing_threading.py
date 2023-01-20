import threading
import sys
import tkinter as tk
import time
import json
import re
from tkinter.font import Font
import socket
from functools import partial

HOST = "10.0.0.2"
PORT = 65432
conn = None
LENGTH_OF_RECV = 37
resp = b""
old_resp = b""
win = tk.Tk()
valve_commands = "abcdefghij"
header_font = Font(family="Montserrat", size=24, weight="bold")
base_font = Font(family="Montserrat", size=18)
win.option_add("*Font", base_font)


HEIGHT = 800
WIDTH = 600
win.title("MACH")
win.geometry(f"{HEIGHT}x{WIDTH}")

p1Value = tk.StringVar()
p2Value = tk.StringVar()
p3Value = tk.StringVar()
_stop = False


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
            while not _stop:
                time.sleep(0.001)
                resp = conn.recv(LENGTH_OF_RECV)
                get_refined_data(resp)
                if not resp:
                    conn.close()
                    sys.exit(1)
            conn.close()


def get_refined_data(new_data: bytes):
    global old_resp
    # print(old_resp.decode("utf=8") + new_data.decode("utf-8"))
    data = re.findall("\{(.*?)\}", old_resp.decode("utf=8") + new_data.decode("utf-8"))
    # print(data)
    if data:
        val = json.loads("{" + data[0] + "}")
        p1Value.set(val["p1"])
        p2Value.set(val["p2"])
        p3Value.set(val["p3"])
        print(f"p1: {val['p1']}", end=" ")
        print(f"p2: {val['p2']}", end=" ")
        print(f"p3: {val['p3']}", end=" ")
        print()
    old_resp = new_data


def connect():
    connection_thread = threading.Thread(target=connection, daemon=True)
    connection_thread.start()


def connected():
    telemetry_text.pack()
    telemetry_frame.pack()
    # telemetry_labels_frame.pack()
    p1Frame.pack(side=tk.LEFT)
    p2Frame.pack(side=tk.LEFT)
    p3Frame.pack(side=tk.LEFT)
    p1label.pack(side=tk.TOP)
    p2label.pack(side=tk.TOP)
    p3label.pack(side=tk.TOP)
    p1text.pack(side=tk.BOTTOM)
    p2text.pack(side=tk.BOTTOM)
    p3text.pack(side=tk.BOTTOM)
    control_frame.pack()
    button_text.pack()
    open_buttons_frame.pack()
    close_buttons_frame.pack()
    for i in range(len(o_buttons)):
        o_buttons[i].pack(side=tk.LEFT)
        c_buttons[i].pack(side=tk.LEFT)
    # open_button.pack()
    # close_button.pack()
    quit_button.pack(side=tk.BOTTOM, pady=20)
    win.title("Connected to BOREALIS")
    connect_button.pack_forget()


def disconnect():
    conn.send(b"quit")
    sys.exit(1)


def button_command(val):
    conn.send(val)


telemetry_frame = tk.Frame(win)
p1Frame = tk.Frame(telemetry_frame)
p2Frame = tk.Frame(telemetry_frame)
p3Frame = tk.Frame(telemetry_frame)
control_frame = tk.Frame(win)
open_buttons_frame = tk.Frame(control_frame)
close_buttons_frame = tk.Frame(control_frame)
o_buttons = []
c_buttons = []
for j in range(10):
    o_buttons.append(
        tk.Button(
            open_buttons_frame,
            text="Open " + str(j + 1),
            # command=lambda: conn.send(f"{valve_commands[i]}".encode("utf-8")),
            command=partial(button_command, f"{valve_commands[j]}".encode("utf-8")),
        )
    )
    c_buttons.append(
        tk.Button(
            close_buttons_frame,
            text="Close " + str(j + 1),
            # command=lambda: conn.send(f"{valve_commands[i]}".encode("utf-8")),
            command=partial(
                button_command, f"{valve_commands[j].upper()}".encode("utf-8")
            ),
        )
    )

# open_button = tk.Button(text="Open Valves", command=lambda: conn.send(b"open"))
# close_button = tk.Button(text="Close Valves", command=lambda: conn.send(b"close"))
connect_button = tk.Button(text="CONNECT TO BOREALIS", command=connect)
quit_button = tk.Button(text="Disconnect", command=disconnect)
telemetry_text = tk.Label(text="Telemetry", font=header_font)
button_text = tk.Label(text="Control", font=header_font)
p1text = tk.Label(p1Frame, textvariable=p1Value)
p2text = tk.Label(p2Frame, textvariable=p2Value)
p3text = tk.Label(p3Frame, textvariable=p3Value)
p1label = tk.Label(p1Frame, text="P1")
p2label = tk.Label(p2Frame, text="P2")
p3label = tk.Label(p3Frame, text="P3")
connect_button.pack()
win.mainloop()
_stop = True
