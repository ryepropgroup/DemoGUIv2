import tkinter as tk

win = tk.Tk() # win equals to a tkinter window
HEIGHT = 600
WIDTH = 480 
win.title("MACH launching rockets!") # window title
win.geometry(f'{HEIGHT}x{WIDTH}')

label = tk.Label(text="Borealis Mission Control!")
data = tk.StringVar()
data.set("hello")
label2 = tk.Label(textvariable=data)
#buttons
def launch_rocket(): # callback to run when btn clicked
	print("🚀🚀🚀")

def abort():
    print("💥💥💥💥")

button = tk.Button(text="Launch", command=launch_rocket)
abortbtn= tk.Button(text="ABORT", command=abort, foreground="#FF0000")


## COMMUNICATION CODE
import socket, time

HOST = "169.254.105.149"
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

label.pack()
label2.pack()
button.pack()
abortbtn.pack()

# def receieve_data():
#         received = conn.recv(1024)
#         # all widgets to be packed to see on the window
#         data.set(received.decode('utf-8'))
#         print(received.decode('utf-8'))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        conn.send(b"Welcome to Borealis Mission Control")

        def receieve_data():
            received = conn.recv(1024)
            # all widgets to be packed to see on the window
            data.set(received.decode('utf-8'))
            if not data:
                return
            print(received.decode('utf-8'))
            win.update()

        while True:
            receieve_data()

