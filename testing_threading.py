import threading, socket, sys
import tkinter as tk

HOST = "10.42.0.40"
PORT = 65432
conn = None
def connection():
    global conn
    global res
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except Exception:
            print("Exception Error: Unable to Open Specified Port: "+str(PORT))
            return
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            # connect_button.pack_forget()
            connected()
#            conn.sendall(b"Welcome to Borealis Mission Control")
            # s.recv()
            while True:
                rec = conn.recv(1024).decode('utf-8')
                res.set(rec)
                if not rec:
                    conn.close()
                    sys.exit(1)


connection_thread = threading.Thread(target=connection, daemon=True)
def connect():
    connection_thread.start()

def connected():
    button.pack()
    button2.pack()
    tex.pack()
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
win.geometry(f'{HEIGHT}x{WIDTH}')
button = tk.Button(text="Open Valves", command=lambda: conn.send(b"open"))
button2 = tk.Button(text="Close Valves", command=lambda: conn.send(b"close"))
res = tk.StringVar()
connect_button = tk.Button(text="CONNECT TO BOREALIS", command=connect)
quit_button = tk.Button(text="Disconnect", command=disconnect)

tex = tk.Label(textvariable=res)
connect_button.pack()
# button.pack()
# tex.pack()

# quit_button.pack()
win.mainloop()


# gui_thread = threading.Thread(target=gui)
# gui_thread.daemon=True
# gui_thread.start()
