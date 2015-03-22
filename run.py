import sys
from TreadmillSpeed import TreadmillSpeed

def main():
    if len(sys.argv) != 2:
        print("Usage: run.py <speed-multiplier>")
        print("Where <speed-multiplier> is a positive multiplier of the speed")
        print("E.g.: python run.py 1.5")
    else:
        tick_length = float(sys.argv[1])
        t = TreadmillSpeed(tick_length=tick_length)
        t.run()
        t.clean()

if __name__ == '__main__':
    main()
