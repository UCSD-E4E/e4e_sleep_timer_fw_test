from time import sleep
from tester.tester import Tester
import random

TEST_PORT = "COM7"
DEBUG_PORT = "COM11"
ECHO_VELOCITY = 500.0

def test_fastSerial():
    tester = Tester(TEST_PORT, debug_port=DEBUG_PORT)
    random.seed(0)
    with tester:
        assert(tester.sendDebugMenuCommand("1").endswith(b'\r\n>'))
        assert(tester.sendDebugMenuCommand("e").endswith(b'\r\n>'))
        random_length = random.randint(1, 128)
        random_data = random.randbytes(random_length)
        tester.debugPort.write(random_data)
        sleep(random_length / ECHO_VELOCITY)
        read_data = tester.flushUSB()
        print(len(read_data))
        assert(random_data == read_data)

def test_multipleRead():
    tester = Tester(TEST_PORT, debug_port=DEBUG_PORT)
    random.seed(0)
    with tester:
        assert(tester.sendDebugMenuCommand("1").endswith(b'\r\n>'))
        assert(tester.sendDebugMenuCommand("e").endswith(b'\r\n>'))
        random_trials = random.randint(1, 32)
        random_length = random.randint(1, 32)
        for i in range(random_trials):
            random_data = random.randbytes(random_length)
            tester.debugPort.write(random_data)
            sleep(random_length / ECHO_VELOCITY)
            read_data = tester.flushUSB()
            assert(random_data == read_data)
            sleep(random.randrange(0, 2.0))

if __name__ == '__main__':
    test_fastSerial()