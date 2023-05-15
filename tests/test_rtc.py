from tester.tester import Tester
import datetime as dt

SERIAL_PORT = "COM7"

def test_ascending():
    tester = Tester(SERIAL_PORT)
    with tester:
        tester.sendDebugMenuCommand('2')
        output = tester.sendDebugMenuCommand('3').decode()
    lines = output.splitlines()[1:-2]
    times = [int(line.split(': ')[1], 16) for line in lines[:-1]]
    assert(len(times) > 100)
    for i in range(len(times) - 1):
        assert(times[i] <= times[i + 1])

def test_setTime():
    tester = Tester(SERIAL_PORT)
    with tester:
        output = tester.sendDebugMenuCommand('2')
        assert(output == b'2\r\n 1: Get RTC Time\r\n 2: Set RTC Time\r\n 3: Hex Clock\r\n 4: Set Alarm\r\n>')
        output = tester.sendDebugMenuCommand('2', ': ')
        assert(output == b'2\r\nUpper Half Time: ')
        now = int(dt.datetime.now().timestamp() * 1000)
        upper = now >> 32
        lower = now & 0x0FFFFFFFF
        output = tester.sendDebugMenuCommand(f'{hex(upper)}\r', ': ', slow=True)
        assert(output.endswith(b'\r\nLower Half Time: '))
        output = tester.sendDebugMenuCommand(f'{hex(lower)}\r', slow=True)
        assert(output.endswith(b'\r\n 2: RTC Debug Menu\r\n>'))
        output = tester.sendDebugMenuCommand('2')
        # assert(output == b'2\r\n 1: Get RTC Time\r\n 2: Set RTC Time\r\n 3: Hex Clock\r\n 4: Set Alarm\r\n>')
        output = tester.sendDebugMenuCommand('1')
        assert(output.endswith(b'\r\n 2: RTC Debug Menu\r\n>'))
        st_time = dt.datetime.fromtimestamp(int(output.decode().splitlines()[1].split(': ')[1], 16) / 1000.0)
        assert(abs((st_time - dt.datetime.now()).total_seconds()) < 5)

def test_setAlarm():
    tester = Tester(SERIAL_PORT)
    with tester:
        # Enter RTC menu
        output = tester.sendDebugMenuCommand('2')
        assert(output == b'2\r\n 1: Get RTC Time\r\n 2: Set RTC Time\r\n 3: Hex Clock\r\n 4: Set Alarm\r\n>')
        output = tester.sendDebugMenuCommand('2', ': ')
        assert(output == b'2\r\nUpper Half Time: ')
        now = int(dt.datetime.now().timestamp() * 1000)
        upper = now >> 32
        lower = now & 0x0FFFFFFFF
        output = tester.sendDebugMenuCommand(f'{hex(upper)}\r', ': ', slow=True)
        assert(output.endswith(b'\r\nLower Half Time: '))
        output = tester.sendDebugMenuCommand(f'{hex(lower)}\r', slow=True)
        assert(output.endswith(b'\r\n 2: RTC Debug Menu\r\n>'))

        alarmTime = dt.datetime.now() + dt.timedelta(seconds=10)

        upper = int(alarmTime.timestamp() * 1000) >> 32
        lower = int(alarmTime.timestamp() * 1000) & 0x0FFFFFFFF

        output = tester.sendDebugMenuCommand('2')
        assert(output == b'2\r\n 1: Get RTC Time\r\n 2: Set RTC Time\r\n 3: Hex Clock\r\n 4: Set Alarm\r\n>')
        output = tester.sendDebugMenuCommand('4', ': ')
        assert(output == b'4\r\nUpper Half Alarm: ')        
        output = tester.sendDebugMenuCommand(f'{hex(upper)}\r', ': ', slow=True)
        assert(output.endswith(b'\r\nLower Half Alarm: '))
        output = tester.sendDebugMenuCommand(f'{hex(lower)}\r', timeout=30, slow=True)
        assert(output.endswith(b'\r\nFlag is now 1\r\n 2: RTC Debug Menu\r\n>'))

if __name__ == '__main__':
    test_setAlarm()