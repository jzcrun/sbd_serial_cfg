from ast import Try
from asyncio.windows_events import NULL
from glob import glob0
from socket import timeout
import sys
from typing import override
from urllib.request import install_opener
# 导入 类
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QApplication, QComboBox, QLabel, QLineEdit
from PyQt5.QtGui import QIcon, QFont

from networkx import is_empty
import serial, threading, time
import serial.tools.list_ports

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

class myComboBox(QWidget):
    def __init__(self, parent, mySerial:mySerial, type):
        super().__init__(parent)
        self.label = QLabel(self)
        self.combo = QComboBox(self)
        self.serial = mySerial
        self.type = type
        self.initUI()

    def initUI(self):
        self.label.resize(100, 30)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.combo.move(self.combo.x() + 110, self.combo.y())
        self.combo.currentIndexChanged.connect(self.selectionChanged1)

    def selectionChanged1(self, i):
        if self.type == 'port':
            self.serial.setPort(f'{self.combo.currentText()}')
        elif self.type == 'baud':
            self.serial.setBaud(int(f'{self.combo.currentText()}'))
        elif self.type == 'databits':
            self.serial.setDatabits(int(f'{self.combo.currentText()}'))
        elif self.type == 'parity':
            parity_dir = ["N", "O", "E"]
            self.serial.setParity(parity_dir[i])
        elif self.type == 'stopbits':
            self.serial.setStopbits(float(f'{self.combo.currentText()}'))

class myButton(QPushButton):
    def __init__(self, parent, mySerial:mySerial, type='start_stop'):
        super().__init__(parent)
        self.serial = mySerial
        self.type = type
        self.initUI()

    def initUI(self):
        self.setStyleSheet("QPushButton { color: black; }")
        if self.type == 'start_stop':
            self.setText('打开串口')
            self.setToolTip("启动串口收发")
        if self.type == 'send':
            self.setText('发送')
            self.setToolTip("发送数据")
        self.clicked[bool].connect(self.handle_clicked)

    @override
    def setGeometry(self, ax:int, ay:int, aw:int, ah:int):
        super().setGeometry(ax, ay, aw, ah)

    def handle_clicked(self):
        if self.type == 'start_stop':
            if self.serial.is_open:
                self.setStyleSheet("QPushButton { color: black; }")
                self.setText('打开串口')
                self.serial.stopRead()
                self.serial.close()
                print(f'close {self.serial.port}')
            else:
                self.setStyleSheet("QPushButton { color: red; }")
                self.setText('关闭串口')
                self.serial.open()
                self.serial.startRead()
                print(f'open {self.serial.port} {self.serial.baudrate} {self.serial.bytesize} {self.serial.parity} {self.serial.stopbits}')
        elif self.type == 'send':
            if self.serial.is_open and not self.serial.output.text() == '':
                self.serial.write(self.serial.output.text().encode())

def read_serial(ser:mySerial):
    while True:
        if ser.is_open:
            if ser.readFlag and ser.in_waiting > 0:
                data = ser.readline().decode('utf-8')  # 读取一行数据，解码为字符串
                print(data)  # 打印数据
                text = ser.input.text()+data
                ser.input.setText(text)
            time.sleep(0.1)  # 等待一段时间继续读取
        time.sleep(0.5)

if __name__ == '__main__':
    # 创建 QApplication 类的实例，并传入命令行参数
    app = QApplication(sys.argv)
    # 创建 QWidget 类的实例，相当于创建一个窗口
    w = QWidget()
    # 设置宽高位置
    w.setGeometry(0, 0, 1920, 1080)

    input =  QLineEdit(w)
    input.setGeometry(40, 290, 400, 400)
    input.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    output =  QLineEdit(w)
    output.setGeometry(450, 290, 400, 400)
    output.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    ser = mySerial(input, output, 0.5)

    QToolTip.setFont(QFont('SansSerif', 10))
    btn1 = myButton(w, ser, 'start_stop')
    btn1.setGeometry(40, 40, 80, 40)

    btn2 = myButton(w, ser, 'send')
    btn2.setGeometry(450, 700, 80, 40)

    portCombo = myComboBox(w, ser, 'port')
    portCombo.label.setText('端口')
    portCombo.setGeometry(140, 40, 700, 30)
    ports = serial.tools.list_ports.comports()
    if not ports:
        portCombo.combo.addItem('None')
    else:
        for port in ports:
            #print(f"{port}: {port.device}")
            portCombo.combo.addItem(f"{port.device}")
    portCombo.combo.setCurrentIndex(0)

    baudCombo = myComboBox(w, ser, 'baud')
    baudCombo.label.setText('波特率')
    baudCombo.setGeometry(140, 80, 300, 30)
    baudList = ["1200", "2400", "4800", "9600", "14400", "19200","38400", "43000", "57600", "76800", "115200", "128000", "230400", "460800"]
    for b in baudList:
        baudCombo.combo.addItem(b)
    baudCombo.combo.setCurrentIndex(3)

    databitsCombo = myComboBox(w, ser, 'databits')
    databitsCombo.label.setText('数据长度')
    databitsCombo.setGeometry(140, 120, 300, 30)
    databitsList = ["5", "6", "7", "8"]
    for d in databitsList:
        databitsCombo.combo.addItem(d)
    databitsCombo.combo.setCurrentIndex(3)

    parityCombo = myComboBox(w, ser, 'parity')
    parityCombo.label.setText('奇偶校验')
    parityCombo.setGeometry(140, 160, 300, 30)
    parityList = ["无", "奇校验", "偶校验"]
    for p in parityList:
        parityCombo.combo.addItem(p)
    parityCombo.combo.setCurrentIndex(0)

    stopbitsCombo = myComboBox(w, ser, 'stopbits')
    stopbitsCombo.label.setText('停止位')
    stopbitsCombo.setGeometry(140, 200, 300, 30)
    stopbitsList = ["1", "1.5", "2"]
    for stop in stopbitsList:
        stopbitsCombo.combo.addItem(stop)
    stopbitsCombo.combo.setCurrentIndex(0)

    # 设置窗口的标题与图标
    w.setWindowTitle('输变电配置')
    app.setWindowIcon(QIcon("./sbd.ico"))

    thread = threading.Thread(target=read_serial, args=(ser,))
    thread.start()

    # 显示窗口
    w.show()
    # 进入程序主循环，并通过 exit 确保主循环安全结束
    sys.exit(app.exec_())
