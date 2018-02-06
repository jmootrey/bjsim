'''
unittesy.py
Handles serial communication and Testing
Bonjoiv Amp

'''


class UnitTest:

    def __init__(self):
        self.im_awake = bytes(['0x04', '0xBA', '0x00'])
        self.im_awake.append(self.crc_check(self.im_awake, 'gemerate'))

    def MakeLink(self, tx=None, rx=None):
        import serial
        try:
            # transmit bus
            self.tx = serial.Serial(port=tx, baudrate=115200, timeout=.4)
            # rec bus
            self.rx = serial.Serial(port=rx, baudrate=115200, timeout=.4)
        except ValueError:
            raise NameError('Illegal Comm Parameter')

    def crc_check(self, d, m='check'):
        # checksum ~(b1 + b2 + b3)+1 & 127
        crc = (~sum(d[0:3])) + 1 & 127
        if crc != d[3]:
            return False
        else:
            if m == 'check':
                return True
            else:
                return crc

    def get_packet(self):
        self.rec = None
        self.c = 0
        while len(self.rec) != 4:
            self.rec = self.rx.read(4)
            self.c += 1
            if self.rec[0] != 4:
                self.rec = None
            elif self.crc_check(self.rec):
                return self.rec
            elif self.c >= 4:
                return False
                break

    def packet_library(d, s='cwr', e='ba'):
        # stuff
        None

    def execute_test(self, test):
        if test == 0:
            self.tx.write(self.im_awake)
            self.response = self.get_packet()
            if self.response:
                    if self.packet_library(self.response, e='ba'):
                        self.response = self.get_packet
                    else:
                        return False
                    if self.packet_library(self.response, e='ad'):




            self.packet = self.get_packet()
