import socket

#ip = "192.168.0.8"
ip = "10.42.0.168"
#ip = "localhost"
port = 12229
#port = 12230
buffer_size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

while True:
    try:
        data = float(s.recv(buffer_size))
        print(data)
    except:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        break



