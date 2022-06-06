import datetime as dt
import logging
from time import sleep
from typing import Optional

import serial

class TimeoutError(Exception):
    pass

class Tester:
    def __init__(self, usb_port: str, *, debug_port: Optional[str] = None):
        self.__log = logging.Logger("Tester")
        self.__usb_port = usb_port
        self.__log.info(f"USB port on {usb_port}")
        self.__debug_port = debug_port
        self.__log.info(f'Debug port on {debug_port}')

    def __enter__(self):
        self.usbPort = serial.Serial(self.__usb_port, baudrate=115200)
        self.__log.info("Initialized USB Port")
        if self.__debug_port:
            self.debugPort = serial.Serial(self.__debug_port, baudrate=115200)
            self.__log.info("Initialized Debug Port")
        else:
            self.debugPort = None
    
    def __exit__(self, *args):
        self.usbPort.close()
        self.__log.info("Closed USB Port")
        if self.debugPort:
            self.debugPort.close()
            self.__log.info("Closed Debug Port")


    def sendDebugMenuCommand(self, cmd: str, prompt: str = ">", timeout: float = 10.0, *, slow: bool = True) -> bytes:
        startTime = dt.datetime.now()
        if not slow:
            self.usbPort.write(cmd.encode())
        else:
            for c in cmd:
                self.usbPort.write(c.encode())
                sleep(0.1)
        response = b''
        self.usbPort.timeout = timeout
        while not response.endswith(prompt.encode()):
            response += self.usbPort.read()
            if (dt.datetime.now() - startTime).total_seconds() > timeout:
                break
        self.__log.info(f"DUT responded to {cmd} with {response.decode(errors='ignore')}")
        return response

    def flushUSB(self, timeout: float=1.0) -> bytes:
        self.usbPort.timeout = timeout
        return self.usbPort.read(self.usbPort.in_waiting)
