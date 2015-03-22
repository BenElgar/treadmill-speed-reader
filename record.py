from TreadmillSpeed import TreadmillSpeed
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: record.py <log-file>")
        print("Where <log-file> is the file where the pin fire times will be recorded to")
        print("E.g.: python record.py fast.log")
    else:
        filename = sys.argv[1]
        t = TreadmillSpeed(record_filename=filename)
        t.run()
        t.clean()

if __name__ == '__main__':
    main()
