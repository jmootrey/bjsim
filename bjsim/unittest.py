'''
unittesy.py
Handles serial communication and Testing
Bonjoiv Amp

'''


class UnitTest:

    def MakeLink(self, tx=None, rx=None):
        import serial
        try:
            # transmit bus
            self.tx = serial.Serial(port=tx, baudrate=115200, timeout=.4)
            # rec bus
            self.rx = serial.Serial(port=rx, baudrate=115200, timeout=.4)
        except ValueError:
            raise NameError('Illegal Comm Parameter')

    def work(self, test):

        if test == 0:
            self.rec = None
            while len(self.rec) != 4:
                self.rec = self.rx.read(4)
                if self.rec[0] != 4:
                    self.rec = None
