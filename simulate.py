import sys
from TreadmillSpeed import TreadmillSpeed

def main():
    if len(sys.argv) != 2:
        print("Usage: simulate.py <log-file>")
        print("Where <log-file> is a log file containing the pin fire times")
        print("E.g.: python simulate.py slow.log")
    else:
        filename = sys.argv[1]
        t = TreadmillSpeed(simulate_filename=filename)
        t.run()
        t.clean()

if __name__ == '__main__':
    main()
