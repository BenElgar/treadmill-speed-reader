import RPi.GPIO as GPIO
from threading import Timer

class TreadmillSpeed:
    count = 0
    treadmill_length = 0.6 # metres
    stream_time = 1 # seconds
    gpio_pin = 3

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.gpio_pin, GPIO.FALLING, callback=self.pinTriggered, bouncetime=100)

    def run(self):
        # Call this every time period
        Timer(self.stream_time, self.streamTriggered).start()

    def pinTriggered(self, channel):
        self.count += 1

    def streamTriggered(self):
        # Call this every time period
        Timer(1, self.streamTriggered).start()

        # Print count and reset it
        print(self.count*self.treadmill_length / self.stream_time)
        self.count = 0

def main():
    T = TreadmillSpeed()
    T.run()
