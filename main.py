#!/usr/bin/env python3
from bjsim import bjsim
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bonjoivi Amp Simulator')
    parser.add_argument('-t', '--tx', help='Transmit Dev (/dev/ttyUSBx)',
                        default='stdout')
    parser.add_argument('-r', '--rx', help='Receive Dev (/dev/ttyUSBx)',
                        default='stdout')
    args = parser.parse_args()
    App = bjsim.BongjoviSimulator(args)
    App.run()
