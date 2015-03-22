import socket

#ip = "192.168.0.8"
#ip = "10.42.0.168"
ip = "localhost"
port = 12229
#port = 12230
buffer_size = 18

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

while True:
    data = float(s.recv(buffer_size))
    print(data)



