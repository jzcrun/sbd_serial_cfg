from typing import override
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QLabel, QLineEdit
from sbdSerial import mySerial

class myComboBox(QWidget):
    def __init__(self, parent, mySerial:mySerial, type):
        super().__init__(parent)
        self.label = QLabel(self)
        self.combo = QComboBox(self)
        self.serial = mySerial
        self.type = type
        self.combaItemNumber = 0
        self.initUI()

    def initUI(self):
        self.label.resize(100, 30)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.combo.move(self.combo.x() + 110, self.combo.y())
        self.combo.currentIndexChanged.connect(self.selectionChanged)

    def selectionChanged(self, i):
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
        if self.type == 'add':
            self.setText('添加采集任务')
            self.setToolTip("添加采集modbus传感器任务，并将采集到的数据通过输变电协议发送")
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
        elif self.type == 'add':
            if self.serial.is_open:
                self.serial.write('hello'.encode())

class myEditLine(QWidget):
    def __init__(self, parent, ser:mySerial, type):
        super().__init__(parent)
        self.serial = ser
        self.label = QLabel(self)
        self.lineEdit = QLineEdit(self)
        self.type = type
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 210, 30)

        self.label.resize(100, 30)
        self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.lineEdit.resize(100, 30)
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lineEdit.move(105, 0)
