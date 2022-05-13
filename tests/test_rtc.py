from tester.tester import Tester
import datetime as dt

def test_ascending():
    tester = Tester("COM4")
    with tester:
        tester.sendDebugMenuCommand('2')
        output = tester.sendDebugMenuCommand('3').decode()
    lines = output.splitlines()[1:-2]
    times = [int(line.split(': ')[1], 16) for line in lines]
    assert(len(times) > 100)
    for i in range(len(times) - 1):
        assert(times[i] <= times[i + 1])

def test_setTime():
    tester = Tester("COM4")
    with tester:
        output = tester.sendDebugMenuCommand('2')
        output = tester.sendDebugMenuCommand('2', ': ')
        now = int(dt.datetime.now().timestamp() * 1000)
        upper = now >> 32
        lower = now & 0x0FFFFFFFF
        output = tester.sendDebugMenuCommand(f'{hex(upper)}\r', ': ', slow=True)
        output = tester.sendDebugMenuCommand(f'{hex(lower)}\r', slow=True)
        output = tester.sendDebugMenuCommand('2')
        output = tester.sendDebugMenuCommand('1')
        st_time = dt.datetime.fromtimestamp(int(output.decode().splitlines()[1].split(': ')[1], 16) / 1000.0)
        assert(abs((st_time - dt.datetime.now()).total_seconds()) < 5)

def test_setAlarm():
    tester = Tester("COM4")
    with tester:
        output = tester.sendDebugMenuCommand('2')
        output = tester.sendDebugMenuCommand('2', ': ')
        now = int(dt.datetime.now().timestamp() * 1000)
        upper = now >> 32
        lower = now & 0x0FFFFFFFF
        output = tester.sendDebugMenuCommand(f'{hex(upper)}\r', ': ', slow=True)
        output = tester.sendDebugMenuCommand(f'{hex(lower)}\r', slow=True)

        alarmTime = dt.datetime.now() + dt.timedelta(seconds=10)

        upper = int(alarmTime.timestamp() * 1000) >> 32
        lower = int(alarmTime.timestamp() * 1000) & 0x0FFFFFFFF

        tester.sendDebugMenuCommand('2')
        tester.sendDebugMenuCommand('4', ': ')
        tester.sendDebugMenuCommand(f'{hex(upper)}\r', ': ', slow=True)
        output = tester.sendDebugMenuCommand(f'{hex(lower)}\r', timeout=30, slow=True)
        print(output)

if __name__ == '__main__':
    test_setAlarm()