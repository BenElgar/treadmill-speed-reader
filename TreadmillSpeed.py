from threading import Timer
import socket, timeit, sched, time

class TreadmillSpeed:
    cooldown    = 0
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
    threads     = []

    # For recording
    record_file = None
    recording   = False

    # For simulation
    log_file    = None
    schedule    = None
    simulating  = False

    def __init__(self, ip='', port=12229, tick_length=0.6, stream_time=0.1, gpio_pin=7, cooldown=0.5, record_filename=None, simulate_filename=None):
        # Initialise class properties
        self.ip          = ip
        self.port        = port
        self.tick_length = tick_length
        self.stream_time = stream_time
        self.s           = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.last_spike  = timeit.default_timer()
        self.cooldown    = cooldown

        # Set up recording
        if record_filename:
            self.record_file = open(record_filename, 'w')
            self.recording = True

        # Set up simulation
        if simulate_filename:
            self.log_file = open(simulate_filename, 'r')
            self.schedule = sched.scheduler(timefunc=timeit.default_timer, delayfunc=time.sleep)
            self.simulating = True

        # Set up GPIO
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(gpio_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP )
            GPIO.add_event_detect(gpio_pin, GPIO.FALLING, callback=self.pinTriggered, bouncetime=20)
        except ImportError:
            pass

        # Set up networking
        self.s.bind((self.ip, self.port))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()


    def run(self):
        thread = Timer(self.stream_time, self.streamTriggered).start()
        self.threads.append(thread)

        if self.recording:
            self.record_file.write(str(timeit.default_timer()) + '\n')

        if self.simulating:
            (start, times) = self.get_times()
            for t in times:
                self.schedule.enter(t-start, 1, self.pinTriggered)
            self.schedule.run()


    def pinTriggered(self, channel=None):
        spike_time = timeit.default_timer()

        if self.recording:
            self.record_file.write(str(spike_time) + '\n')
            print(spike_time)
        else:
            self.spike_gap = spike_time - self.last_spike
            self.last_spike = spike_time

    def get_times(self):
        data = self.log_file.readlines()
        data = list(map(str.strip, data))
        data = list(map(float, data))
        start = data[0]
        times = data[1:]
        return (start, times)

    def streamTriggered(self):
        # Call this every time period
        thread = Timer(self.stream_time, self.streamTriggered).start()
        self.threads.append(thread)
        print(self.threads)

        if self.spike_gap:
            if self.last_spike > timeit.default_timer() - self.cooldown:
                speed = self.tick_length/self.spike_gap
            else:
                speed = 0.00
            print(speed)
            self.streamSend(speed)

    def streamSend(self, speed):
        self.conn.send(str(speed).encode())


    def clean(self):
        # Wait for all threads to finish
        [x.join() for x in self.threads]

        if self.recording:
            self.record_file.close()

        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        print("cleaned")

def main():
    T = TreadmillSpeed(record_filename='slow.log')
    try:
        T.run()
    finally:
        #T.clean()
        exit()

if __name__ == "__main__":
    main()
