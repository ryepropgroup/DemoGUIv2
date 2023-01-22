# allows different parts of program to run concurrently
import threading

# provides various fucntions and variables that are used to manipulate diff parts of
# the python runtime environment

import sys

# import tkinter GUI
import tkinter as tk

# adds time module, allowing python to work with time
import time

# module that enables us to work with JSON data
import json

# module that provides regular expression matching operations
import re

# allows us to work with fonts FROM tkinter module
from tkinter.font import Font

#
import socket
from functools import partial
from collections import deque

from PIL import ImageTk, Image


HOST = "127.0.0.1"
PORT = 65432
conn = None
LENGTH_OF_RECV = 64
resp = b""
old_resp = b""
win = tk.Tk()
valve_commands = "abcdefghij"
header_font = Font(family="Montserrat", size=24, weight="bold")
base_font = Font(family="Montserrat", size=18)
button_font = Font(family="Montserrat", size=14)
win.option_add("*Font", base_font)


HEIGHT = 600
WIDTH = 1000
win.title("MACH")
win.geometry(f"{WIDTH}x{HEIGHT}")

p1Value = tk.StringVar()
p2Value = tk.StringVar()
p3Value = tk.StringVar()
p1ValueMin = tk.StringVar()
p2ValueMin = tk.StringVar()
p3ValueMin = tk.StringVar()
_stop = False
p1Rolling = deque([], maxlen=100)
p2Rolling = deque([], maxlen=100)
p3Rolling = deque([], maxlen=100)


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
        p1Rolling.append(int(val["p1"]))
        p2Rolling.append(int(val["p2"]))
        p3Rolling.append(int(val["p3"]))
        p1Value.set("MAX: " + str(max(p1Rolling)))
        p2Value.set("MAX: " + str(max(p2Rolling)))
        p3Value.set("MAX: " + str(max(p3Rolling)))
        p1ValueMin.set("MIN: " + str(min(p1Rolling)))
        p2ValueMin.set("MIN: " + str(min(p2Rolling)))
        p3ValueMin.set("MIN: " + str(min(p3Rolling)))
        p1text.config(foreground=get_color("p1", max(p1Rolling)))
        p2text.config(foreground=get_color("p2", max(p1Rolling)))
        p3text.config(foreground=get_color("p3", max(p1Rolling)))
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
    p1Frame.pack(side=tk.LEFT, padx=40)
    p2Frame.pack(side=tk.LEFT, padx=40)
    p3Frame.pack(side=tk.LEFT, padx=40)
    p1label.pack(side=tk.TOP)
    p2label.pack(side=tk.TOP)
    p3label.pack(side=tk.TOP)
    p1text.pack(side=tk.BOTTOM)
    p1textmin.pack(side=tk.BOTTOM)
    p2text.pack(side=tk.BOTTOM)
    p2textmin.pack(side=tk.BOTTOM)
    p3text.pack(side=tk.BOTTOM)
    p3textmin.pack(side=tk.BOTTOM)
    button_text.pack()
    control_frame.pack()
    open_buttons_frame.pack()
    on_text.pack()
    close_buttons_frame.pack()
    off_text.pack()
    
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


def get_color(pressure, x):
    red = "#f00"
    green = "#0f0"
    orange = "#f80"
    if pressure == "p1":
        if x >= 2500:
            return red
        elif x >= 2300:
            return orange
    elif pressure == "p2":
        if x >= 1600:
            return red
        elif x >= 1400:
            return orange
    elif pressure == "p3":
        if x >= 1600:
            return red
        elif x >= 1400:
            return orange
    return green


def button_command(val):
    conn.send(val)


telemetry_frame = tk.Frame(win)
p1Frame = tk.Frame(telemetry_frame)
p2Frame = tk.Frame(telemetry_frame)
p3Frame = tk.Frame(telemetry_frame)
control_frame = tk.Frame(win)
open_buttons_frame = tk.Frame(control_frame)
open_buttons_frame["pady"]=20
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
            font=button_font,
            padx=10,
            pady=10
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
            font=button_font,
            padx= 10,
            pady=10
        )
    )

# open_button = tk.Button(text="Open Valves", command=lambda: conn.send(b"open"))
# close_button = tk.Button(text="Close Valves", command=lambda: conn.send(b"close"))
img = ImageTk.PhotoImage(Image.open("mach_logo.png"))
image_label = tk.Label(image=img)
connect_button = tk.Button(text="CONNECT TO BOREALIS", command=connect)
quit_button = tk.Button(text="Disconnect", command=disconnect)
telemetry_text = tk.Label(text="Telemetry", font=header_font)
button_text = tk.Label(text="Control", font=header_font)
on_text = tk.Label(open_buttons_frame,text="On", font=header_font)
off_text = tk.Label(close_buttons_frame,text="Off", font=header_font)
p1text = tk.Label(p1Frame, textvariable=p1Value)
p2text = tk.Label(p2Frame, textvariable=p2Value)
p3text = tk.Label(p3Frame, textvariable=p3Value)
p1textmin = tk.Label(p1Frame, textvariable=p1ValueMin)
p2textmin = tk.Label(p2Frame, textvariable=p2ValueMin)
p3textmin = tk.Label(p3Frame, textvariable=p3ValueMin)
p1label = tk.Label(p1Frame, text="P1")
p2label = tk.Label(p2Frame, text="P2")
p3label = tk.Label(p3Frame, text="P3")
image_label.pack()
connect_button.pack()
win.mainloop()
_stop = True
