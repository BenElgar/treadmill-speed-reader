import socket

ip = "10.42.0.168"
ip = "localhost"
port = 12229
buffer_size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

while True:
    try:
        data = float(s.recv(buffer_size))
        print(data)
    except:
        break
    finally:
        s.close



