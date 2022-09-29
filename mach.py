import tkinter as tk

win = tk.Tk() # win equals to a tkinter window
HEIGHT = 600
WIDTH = 480 
win.title("MACH launching rockets!") # window title
win.geometry(f'{HEIGHT}x{WIDTH}')

label = tk.Label(text="This is Mission Control GUI!")

#buttons
def launch_rocket(): # callback to run when btn clicked
	print("🚀🚀🚀")

def abort():
    print("💥💥💥💥")

button = tk.Button(text="Launch", command=launch_rocket)
abortbtn= tk.Button(text="ABORT", command=abort, foreground="#FF0000")

# all widgets to be packed to see on the window
label.pack()
button.pack()
abortbtn.pack()

win.mainloop()
