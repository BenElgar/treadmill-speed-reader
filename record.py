from TreadmillSpeed import TreadmillSpeed
import sys


def main():
    filename = sys.argv[1]
    t = TreadmillSpeed(record_filename=filename)
    t.run()
    t.clean()

if __name__ == '__main__':
    main()
