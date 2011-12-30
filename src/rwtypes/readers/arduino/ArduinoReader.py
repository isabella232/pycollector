import time
import serial

from __reader import Reader

class ArduinoReader(Reader):
    def setup(self):
        if not hasattr(self, 'interface'):
            self.interface = '/dev/ttyUSB0'
        if not hasattr(self, 'bps'):
            self.bps = 9600
        self.arduino = serial.Serial(self.interface, self.bps)

    def read(self):
        while True:
            try:
                msg = "%s,%s" % (time.time(), self.arduino.readline())
                self.store(msg)
            except Exception, e:
                print 'error reading'
                print e
