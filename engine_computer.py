import socket, time, serial 

HOST = "169.254.205.14"
# The servers hostname or IP address
PORT = 65432 # The port used by the server

# arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect ((HOST, PORT))
    data = s.recv(1024)
    print(data.decode('utf-8'))
    if data.decode('utf-8') == 'Welcome to Borealis Mission Control':
        while True:
            data = s.recv(1024)
            print(data.decode('utf-8'))
            if data == b"Open":
                s.sendall(b'valves opened')
            if data == b"quit":
                s.close()
                exit()