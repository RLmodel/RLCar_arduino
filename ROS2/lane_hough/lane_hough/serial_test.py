#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial


class serial_test():
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyNANO", 115200)
        self.op = "up"
        self.ser.write(self.op.encode())

    def display(self):
        ser = self.ser
        line = ser.readline()
        decoded_line = line.decode('utf-8').rstrip()
        print(decoded_line)


def main():
    serial_ins = serial_test()
    
    while True:
        serial_ins.display()

if __name__== "__main__":
    main()