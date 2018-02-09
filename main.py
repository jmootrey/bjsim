#!/usr/bin/env python3
from bjsim import bjsim
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bonjoivi Amp Simulator')
    requiredNamed = parser.add_argument_group('Required:')
    requiredNamed.add_argument('-t', '--tx', help='Transmit Dev (/dev/ttyUSBx)',
                        default='stdout', required=True)
    requiredNamed.add_argument('-r', '--rx', help='Receive Dev (/dev/ttyUSBx)',
                        default='stdout', required=True)
    args = parser.parse_args()
    App = bjsim.BongjoviSimulator(args)
    App.run()
