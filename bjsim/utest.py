'''
unittesy.py
Handles serial communication and Testing
Bonjoiv Amp

'''
import serial

class Utest:


    def MakeLink(self, tx, rx):
        try:
            # transmit bus
            self.tx = serial.Serial(port=tx, baudrate=115200, timeout=.4)
            # rec bus
            self.rx = serial.Serial(port=rx, baudrate=115200, timeout=.4)
            return True
        except ValueError:
            return NameError('Illegal Comm Parameter')

    def crc_check(self, d, m='check'):
        # checksum ~(b1 + b2 + b3)+1 & 127
        self.crc = (~sum(d[0:3])) + 1 & 127
        if m == 'check':
            if self.crc != d[3]:
                return False
            else:
                return True
        else:
            return self.crc

    def get_packet(self, attempts=2, f=True):
        self.rec = []
        self.crc_error = 0
        self.c = 0
        if f: self.rx.flushInput()
        while True:
            self.rec = self.rx.read(4)
            self.c += 1
            if self.rec:
                if self.rec[0] == 2:
                    if self.crc_check(self.rec):
                        return self.rec
                    else:
                        self.crc_error += 1
            if self.c >= attempts:
                if self.crc_error == 0:
                    return False
                else:
                    return self.crc_error

    # Compare data packet to expected return t/f
    def packet_library(self, msg=None):
        if self.msg == int('0x17', 16):  # Cabin Volume
            self.tx.write(self.packet_library('volume'))
        if self.msg == 0:  # Cabin Mute
            pass
        if self.msg == int('0x08', 16):  # Soure Select
            pass
        if self.msg == int('0x01', 16):  # Master Source to 2
            pass
        if self.msg == int('0x02', 16):  # Headphone Select
            pass
        if self.msg == int('0x1C', 16):  # Cabin Bass
            pass
        if self.msg == int('0x1D', 16):  # Cabin Treble
            pass
        if self.msg == int('0x03', 16):  # Cabin Profile
            pass
        if self.msg == int('0x17', 16):  # Get Version
            pass

    # Initiate communication with CWR450, return packet following init.
    def handshake(self):
        self.im_awake = bytes([0x04, 0xBA, 0x00, 0x42])
        self.tx.write(self.im_awake)
        while True:
            self.r = self.get_packet(attempts=4)
            if self.r:
                break

        self.r = self.response_handler(d=self.r, e='0xba', r=False)
        return self.r

    def packet_assembly(self, d=None):
        self.rtn = bytes([0x04, d[1], d[2]])
        self.rtn.append(self.crc_check(self.rtn, 'gen'))
        return self.rtn

    # Gen response handler. d=data_packet e=expected packet type
    # r = supply sane response to bus
    def response_handler(self, d=None, e=None, r=True):
        if r and e == hex(d[1]):
            self.tx.write(self.packet_assembly(d))
            return True
        elif not r and e == d[1]:
            return True
        elif not e and r:
            self.rtn = self.packet_assembly(d)
            self.tx.write(self.rtn)
            return self.rtn
        else:
            return False



'''
            if self.msg == int('0x17', 16):  # Cabin Volume
                pass
            if self.msg == 0:  # Cabin Mute
                pass
            if self.msg == int('0x08', 16):  # Soure Select
                pass
            if self.msg == int('0x01', 16):  # Master Source to 2
                pass
            if self.msg == int('0x02', 16):  # Headphone Select
                pass
            if self.msg == int('0x1C', 16):  # Cabin Bass
                pass
            if self.msg == int('0x1D', 16):  # Cabin Treble
                pass
            if self.msg == int('0x03', 16):  # Cabin Profile
                pass
            if self.msg == int('0x17', 16):  # Get Version
                pass

if self.e == int('0x17', 16):
    pass

        return False
'''
