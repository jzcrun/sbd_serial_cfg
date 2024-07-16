import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QLineEdit

class mySerial(serial.Serial):
    def __init__(self, input:QLineEdit, output:QLineEdit, readtime, port = None, baud:int=9600, databits:int=8, parity:str="N", stopbits:int=1):
        super().__init__(port, baud, databits, parity, stopbits, timeout=readtime)
        self.close()
        self.input = input
        self.output = output
        self.readFlag = False
        self.set_buffer_size(16*1024, 16*1024)
    
    def setPort(self, port):
        if self.is_open:
            self.close()
            self.port = port
            self.open()
            print(f'open new port {self.port}')
        else:
            self.port = port

    def setBaud(self, baud):
        if self.is_open:
            self.close()
            self.baudrate = baud
            self.open()
            print(f'open port {self.port} new baud {self.baudrate}')
        else:
            self.baudrate = baud

    def setDatabits(self, databits):
        if self.is_open:
            self.close()
            self.bytesize = databits
            self.open()
            print(f'open port {self.port} new bytesize {self.bytesize}')
        else:
            self.bytesize = databits

    def setParity(self, parity):
        if self.is_open:
            self.close()
            self.parity = parity
            self.open()
            print(f'open port {self.port} new parity {self.parity}')
        else:
            self.parity = parity

    def setStopbits(self, stopbits):
        if self.is_open:
            self.close()
            self.stopbits = stopbits
            self.open()
            print(f'open port {self.port} new stopbits {self.stopbits}')
        else:
            self.stopbits = stopbits

    def startRead(self):
        self.readFlag = True

    def stopRead(self):
        self.readFlag = False