import socket

ip = "localhost"
port = 12229
buffer_size = 18

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

while True:
    data = float(s.recv(buffer_size))
    print(data)



