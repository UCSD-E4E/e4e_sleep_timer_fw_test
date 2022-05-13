from time import sleep
from tester.tester import Tester
import random

def test_fastSerial():
    tester = Tester("COM4", debug_port="COM5")
    random.seed(0)
    with tester:
        tester.sendDebugMenuCommand("1")
        tester.sendDebugMenuCommand("e")
        random_length = random.randint(1, 128)
        random_data = random.randbytes(random_length)
        tester.debugPort.write(random_data)
        read_data = tester.flushUSB()
        print(len(read_data))
        assert(random_data == read_data)

def test_multipleRead():
    tester = Tester("COM4", debug_port="COM5")
    random.seed(0)
    with tester:
        tester.sendDebugMenuCommand("1")
        tester.sendDebugMenuCommand("e")
        random_trials = random.randint(1, 32)
        random_length = random.randint(1, 32)
        for i in range(random_trials):
            random_data = random.randbytes(random_length)
            tester.debugPort.write(random_data)
            read_data = tester.flushUSB()
            assert(random_data == read_data)
            sleep(random.randrange(0, 2.0))

if __name__ == '__main__':
    test_fastSerial()