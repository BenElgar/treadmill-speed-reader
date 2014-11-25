import RPi.GPIO as GPIO
from threading import Timer
import socket

class TreadmillSpeed:
    count       = None
    tick_length = None
    stream_time = None
    gpio_pin    = None
    ip          = None
    port        = None
    conn        = None
    addr        = None
    s           = None # Socket object

    def __init__(self, ip='10.42.0.84', port=12345, tick_length=0.6, stream_time=1, gpio_pin=3):
        # Initialise class properties
        self.ip          = ip
        self.port        = port
        self.tick_length = tick_length
        self.stream_time = stream_time
        self.s           = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set up GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.gpio_pin, GPIO.FALLING, callback=self.pinTriggered, bouncetime=100)

        # Set up networking
        self.s.bind((self.ip, self.port))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()

    def run(self):
        Timer(self.stream_time, self.streamTriggered).start()

    def pinTriggered(self, channel):
        self.count += 1

    def streamTriggered(self):
        # Call this every time period
        Timer(self.stream_time, self.streamTriggered).start()

        speed = self.count*self.tick_length / self.stream_time
        print(speed)
        self.conn.send(str(speed).encode())
        self.count = 0

    def __del__(self):
        self.s.close()

def main():
    T = TreadmillSpeed()
    T.run()

if __name__ == "__main__":
    main()
