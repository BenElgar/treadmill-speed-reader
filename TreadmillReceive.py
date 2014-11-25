import socket

ip = "10.42.0.84"
port = 12345
buffer_size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

try:
    while True:
        data = float(s.recv(buffer_size))
        print(data)
except:
    break
finally:
    s.close



