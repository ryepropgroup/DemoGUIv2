import threading, socket

HOST = "127.0.0.1"
PORT = 65432
conn = None
res = ""
def connection():
    global conn
    global res
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except Exception:
            print("quitting")
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            conn.sendall(b"Welcome to Borealis Mission Control")
            # s.recv()
            while True:
                res = conn.recv(1024).decode('utf-8')
                if not res:
                    break
                # win.update()


connection_thread = threading.Thread(target=connection, daemon=True)
def start_connection_thread():
    connection_thread.start()

# connection_thread.daemon=True
import tkinter as tk
# def gui():
win = tk.Tk()
HEIGHT = 600
WIDTH = 480 
win.title("MACH")
win.geometry(f'{HEIGHT}x{WIDTH}')
button = tk.Button(text="Launch", command=lambda: conn.send(b"hello"))

connect_button = tk.Button(text="CONNECT TO BOREALIS", command=start_connection_thread)
quit_button = tk.Button(text="QUIT", command=lambda: conn.send(b"quit"))

tex = tk.Label(text=res)
connect_button.pack()
button.pack()
tex.pack()

quit_button.pack()
win.mainloop()


# gui_thread = threading.Thread(target=gui)
# gui_thread.daemon=True
# gui_thread.start()
