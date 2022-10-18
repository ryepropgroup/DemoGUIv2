import threading, socket, sys
import tkinter as tk

HOST = "169.254.205.14"
PORT = 65432
conn = None
def connection():
    global conn
    global res
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except Exception:
            print("unable to open port on host")
            return
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            # connect_button.pack_forget()
            connected()
            conn.sendall(b"Welcome to Borealis Mission Control")
            # s.recv()
            while True:
                rec = conn.recv(1024).decode('utf-8')
                res.set(rec)
                if not rec:
                    sys.exit(1)


connection_thread = threading.Thread(target=connection, daemon=True)
def connect():
    try:
        print("Waiting to connect...")
        connection_thread.start()
    except:
        print("Already waiting...")
        # pass

def connected():
    button.pack()
    tex.pack()
    quit_button.pack()
    win.title("Connected to BOREALIS")
    connect_button.pack_forget()

def disconnect():
    conn.send(b"quit")
    sys.exit(1)
    connect_button.pack()

win = tk.Tk()
HEIGHT = 600
WIDTH = 480 
win.title("MACH")
win.geometry(f'{HEIGHT}x{WIDTH}')
button = tk.Button(text="Launch", command=lambda: conn.send(b"Open"))
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
