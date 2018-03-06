'''
unittesy.py
Handles serial communication and Testing
Bonjoiv Amp

'''
import serial
import time
from random import random


class Utest:

    def __init__(self, tx, rx):
       self.tx = tx
       self.rx = rx
       self.logfile = 'caplog.log'
       # self.pdic = {23:1, 0:1, 8:None, 1:2, 10:None,
       #             28:None,29:None,3:None, 2:2}
       self.pdic = {23:1, 0:1, 8:1, 1:2, 10:1,
                    28:1,29:1,3:1, 2:2}
    
    def log_facility(self, message):
        with open(self.logfile, mode='w') as self.f:
            self.f.write(message)


    
    def RunTest(self, id):
        self.results = 'Ok'
        # Late Reply Operating
        if id == 1:
            self.results = ' Ok'
            self.timeout = time.time() + 60 * 5
            if not self.handshake():
                    self.results = ' Failed Handshake'
            else:
                while time.time() < self.timeout:
                    if random() > .1:
                       time.sleep(.4)
                    self.p = self.get_packet(f=False, attempts=1)
                    if self.p:
                        self.r = self.response_handler(self.p, e=None)
                        
            return self.results
        # Normal Reply
        elif id == 0:
            self.results = ' Ok'
            self.timeout = time.time() + 60 * 5
            if not self.handshake():
                    self.results = ' Failed Handshake'
            else:
                while time.time() < self.timeout:
                    self.p = self.get_packet(f=False, attempts=1)
                    self.log_facility('Rx: ' + str(self.p))
                    if self.p:
                        self.r = self.response_handler(self.p, e=None)
                        self.results = ' Ok'
            return self.results
        elif id == 2:
            return ' Ok'

    def MakeLink(self, m='o'):
        if m == 'o':
            try:
                # transmit bus
                self.tx = serial.Serial(port=self.tx, baudrate=115200, timeout=.4)
                # rec bus
                self.rx = serial.Serial(port=self.rx, baudrate=115200, timeout=.4)
                return True
            except ValueError:
                return NameError('Illegal Comm Parameter')
            else:
                if self.tx:
                    self.tx.close()
                if self.rx:
                    self.rx.close()

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

    def flushbuffer(self):
        self.rx.flushInput()

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

                    
    # Initiate communication with CWR450, return packet following init.
    def handshake(self):
        self.im_awake = bytes([0x04, 0xBA, 0x00, 0x42])
        self.flushbuffer()
        self.tout=10
        while True:
            self.tx.write(self.im_awake)
            self.r = self.get_packet(attempts=1, f=False)
            if self.r:
                self.r = self.response_handler(d=self.r, e='0xba', r=False)
                if self.r:
                    break
                else:
                    self.tout -= 1
            if self.tout == 0:
                    self.r = False
        
        return self.r

    def packet_assembly(self, d=None):
        self.rtn = bytearray([0x04, d[1], d[2]])
        self.rtn.append(self.crc_check(self.rtn, 'gen'))
        return self.rtn

    # Gen response handler. d=data_packet e=expected packet type
    # r = supply sane response to bus
    def response_handler(self, d=None, e=None, r=True):
        d=bytearray(d)
        if d[2] != 255 and d[1] in self.pdic:
            self.pdic[d[1]]=d[2]
        if r and e == hex(d[1]):
            self.tx.write(self.packet_assembly(d))
            return True
        elif not r and int(e, 16) == d[1]:
            return True
        elif not e and r:
            if d[2] == 255:
                d[2] = self.pdic[d[1]]
            self.rtn = self.packet_assembly(d)
            self.log_facility('Tx: ' + str(self.rec))
            self.tx.write(self.rtn)
            return self.rtn
        else:
            return False