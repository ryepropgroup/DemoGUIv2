import socket, time
HOST = "127.0.0.1"
# The server's hostname or IP address
PORT = 65432 # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect ((HOST, PORT))
    full = ''
    data = s.recv(1024)
    if data.decode( 'utf-8') == 'welcome to Borealis Mission Control':
        while True:
            s.send(bytes(f' (time.time ()!', 'utf-8'))
            print(f"sent data")
            time.sleep(1)