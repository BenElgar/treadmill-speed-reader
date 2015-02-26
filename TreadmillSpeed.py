import RPi.GPIO as GPIO
from threading import Timer
import socket, timeit

class TreadmillSpeed:
    count       = 0
    tick_length = None
    stream_time = None
    gpio_pin    = None
    ip          = None
    port        = None
    conn        = None
    addr        = None
    s           = None # Socket object
    last_spike  = None
    spike_gap   = None

    def __init__(self, ip='10.42.0.84', port=12229, tick_length=0.6, stream_time=1, gpio_pin=7):
        # Initialise class properties
        self.ip          = ip
        self.port        = port
        self.tick_length = tick_length
        self.stream_time = stream_time
        self.s           = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.last_spike  = timeit.default_timer()

        # Set up GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP )
        GPIO.add_event_detect(gpio_pin, GPIO.FALLING, callback=self.pinTriggered, bouncetime=20)

        # Set up networking
        self.s.bind((self.ip, self.port))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()

    def run(self):
        Timer(self.stream_time, self.streamTriggered).start()

    def pinTriggered(self, channel):
        spike_time = timeit.default_timer()
        self.spike_gap = spike_time - self.last_spike
        self.last_spike = spike_time


    def streamTriggered(self):
        # Call this every time period
        Timer(self.stream_time, self.streamTriggered).start()

        speed = self.tick_length/self.spike_gap
        print(speed)
        self.conn.send(str(speed).encode())
        self.count = 0

    def clean(self):
        self.s.close()

def main():
    T = TreadmillSpeed()
    try:
        T.run()
    except:
        T.clean()
        exit()

if __name__ == "__main__":
    main()
