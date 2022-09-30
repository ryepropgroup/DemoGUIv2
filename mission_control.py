import socket, time

HOST = "10.0.0.170"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        conn.send(b"Welcome to Borealis Mission Control")
        while True:
            data = conn.recv(1024)
            print(data.decode('utf-8'))