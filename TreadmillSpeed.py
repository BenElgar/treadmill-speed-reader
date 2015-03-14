from threading import Timer
import socket, timeit, sched, time, collections

class TreadmillSpeed:
    speed_method = None
    __threads    = []
    spike_buffer = None
    running      = False

    def __init__(self, ip='', port=12229, tick_length=0.6, stream_time=0.1, gpio_pin=7, cooldown=0.5, record_filename=None, simulate_filename=None):
        """!
        Initialisation function

        @param ip The IP address of the device running this class. Will default to the default network device's IP address. Should probably be left blank.
        @param port Specifies the port over which the class should connect
        @param tick_length Specifies a multiplier for the outputted speed
        @param stream_time Specifies how often the class should should output a speed
        @param gpio_pin Specifies the GPIO pin on the Raspberry Pi (BOARD mode) that the treadmill is connected to
        @param cooldown Specifies the cooldown between pin triggers
        @param record_filename Specifies the file which pin triggers should be recorded to.
        @param simulate_filename Specifies the log file from which the pin triggers should be simulated.
        """
        # Initialise class properties
        self.ip          = ip
        self.port        = port
        self.tick_length = tick_length
        self.stream_time = stream_time
        self.s           = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cooldown    = cooldown

        # Set up recording
        if record_filename:
            self.record_file = open(record_filename, 'w')
            self.recording = True
        else:
            self.recording = False

        # Set up simulation
        if simulate_filename:
            self.simulate_file = open(simulate_filename, 'r')
            self.schedule = sched.scheduler(timefunc=timeit.default_timer, delayfunc=time.sleep)
            self.simulating = True
        else:
            self.simulating = False

        # Set up GPIO
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(gpio_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP )
            GPIO.add_event_detect(gpio_pin, GPIO.FALLING, callback=self.__pin_triggered, bouncetime=20)
        except ImportError:
            pass

        print("Waiting for connection")

        # Set up networking
        self.s.bind((self.ip, self.port))
        self.s.listen(1)
        self.conn, _ = self.s.accept()

        print("Connected")


    def run(self, speed_method='average_gap', spike_buffer_count=10):
        """!Reads, records or simulates the treadmill
        @param speed_method A currently unused parameter that will be used to select a speed method
        @param spike_buffer_count Specifies the number of spikes over which to average the gap

        If the record_filename is specified then this records to the specified file.
        If the simulate_filename is specified then this simulates the treadmill from the specified log file.
        The treadmill speed is sent across the sockets to the treadmill receive script
        """

        self.running = True
        self.speed_method = speed_method
        self.spike_buffer = collections.deque(maxlen = spike_buffer_count)
        self.spike_buffer.append(timeit.default_timer())


        thread = Timer(self.stream_time, self.__stream_triggered)
        thread.start()
        self.__threads.append(thread)

        if self.recording:
            self.record_file.write(str(timeit.default_timer()) + '\n')

        if self.simulating:
            (start, times) = self.__get_times()
            for t in times:
                self.schedule.enter(t-start, 1, self.__pin_triggered, [])
            self.schedule.run()


    def __pin_triggered(self, channel=None):
        if self.running:
            spike_time = timeit.default_timer()

            if self.recording:
                self.record_file.write(str(spike_time) + '\n')
                print(spike_time)
            else:
                self.spike_buffer.append(spike_time)

    def __get_times(self):
        """
        Get the list of times out of the log file.
        """
        data = self.simulate_file.readlines()
        data = list(map(str.strip, data))
        data = list(map(float, data))
        start = data[0]
        times = data[1:]
        return (start, times)

    def __stream_triggered(self):
        """
        Callback triggered to stream the treadmill speed and setup the next streaming callback
        """
        # Call this every time period
        thread = Timer(self.stream_time, self.__stream_triggered)
        thread.start()
        self.__threads.append(thread)

        if len(self.spike_buffer) > 2:
            speed = self.__get_speed()
            print(speed)
            self.__stream_send(speed)

    def __get_speed(self):
        """
        Calculates the current speed of the treadmill
        """
        if self.speed_method == 'average_gap':
            total_gap = 0
            for i in range(1, len(self.spike_buffer)):
                total_gap += self.spike_buffer[i] - self.spike_buffer[i-1]

            average_gap = total_gap / len(self.spike_buffer)


            if self.spike_buffer[-1] > timeit.default_timer() - self.cooldown:
                speed = self.tick_length/average_gap
            else:
                speed = 0.00

        return speed


    def __stream_send(self, speed):
        """
        Streams the provided speed
        """
        print(speed)
        self.conn.send(str(speed).zfill(18).encode())

    def clean(self):
        """
        Cleans up the connections and closes the files
        """
        # Wait for all threads to finish
        [x.join() for x in self.__threads]

        if self.recording:
            self.record_file.close()

        if self.simulating:
            self.simulate_file.close()

        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        print("Cleaned")

def main():
    T = TreadmillSpeed()
    T.run()
    T.clean()


if __name__ == "__main__":
    main()
