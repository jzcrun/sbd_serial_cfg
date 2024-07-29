import time
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
        elif self.type == 'send':
            self.setText('发送')
            self.setToolTip("发送数据")
        elif self.type == 'ATsend':
            self.setText('发送AT指令')
            self.setToolTip("发送数据结尾添加换行标志")
        elif self.type == 'clear':
            self.setText('清空接收')
            self.setToolTip("清空接收到的数据")
        elif self.type == 'add':
            self.setText('添加采集任务')
            self.setToolTip("添加采集modbus传感器任务，并将采集到的数据通过输变电协议发送")
        elif self.type == 'del':
            self.setText('取消采集任务')
            self.setToolTip("取消采集modbus传感器任务")
        elif self.type == 'TouChuan1':
            self.setText('进入/退出LoRa透传模式')
            self.setToolTip("进入/退出LoRa透传模式")
        elif self.type == 'TouChuan2':
            self.setText('进入/退出Sensor透传模式')
            self.setToolTip("进入/退出Sensor透传模式")
        elif self.type == 'reboot':
            self.setText('重启节点')
            self.setToolTip("重启节点")

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
            cmd = self.serial.output.toPlainText()
            if self.serial.is_open and not self.serial.output.toPlainText() == '':
                #self.serial.write(self.serial.output.toPlainText().encode())
                while len(cmd) > 32:
                    self.serial.write(cmd[0:32].encode())
                    time.sleep(1.5)
                    cmd = cmd[32:]

                if len(cmd) > 0:
                    self.serial.write(cmd.encode())
        elif self.type == 'ATsend':
            if self.serial.is_open and not self.serial.output.toPlainText() == '':
                self.serial.write((self.serial.output.toPlainText() + '\r\n').encode())
        elif self.type == 'clear':
            self.serial.input.clear()
        elif self.type == 'TouChuan1':
            if self.serial.is_open:
                self.serial.write('+++'.encode())
        elif self.type == 'TouChuan2':
            if self.serial.is_open:
                self.serial.write('***'.encode())
        elif self.type == 'reboot':
            if self.serial.is_open:
                self.serial.write('set,reboot'.encode())

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

class myEditLineWithButton(QWidget):
    def __init__(self, parent, ser:mySerial, type):
        super().__init__(parent)
        self.serial = ser
        self.button = QPushButton(self)
        self.lineEdit = QLineEdit(self)
        self.type = type
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 280, 30)
        self.button.resize(150, 30)
        self.lineEdit.resize(120, 30)
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lineEdit.move(155, 0)

        if self.type == 'setCycle':
            self.button.setText('设置上报周期(s)')
            self.lineEdit.setText('10')
        elif self.type == 'setAddr':
            self.button.setText('设置设备地址')
            self.lineEdit.setText('010203040506')
        elif self.type == 'setChn':
            self.button.setText('设置通道(0~80)')
            self.lineEdit.setText('1')

        self.button.clicked[bool].connect(self.handle_clicked)

    def handle_clicked(self):
        if self.type == 'setCycle':
            cmd = 'set,cycle,' + self.lineEdit.text()
        elif self.type == 'setAddr':
            cmd = 'set,id,' + self.lineEdit.text()  
        elif self.type == 'setChn':
            cmd = 'set,channel,' + self.lineEdit.text()
        else:
            cmd = 'hello'

        if self.serial.is_open:
            self.serial.write(cmd.encode())

def relativeMove(obj, dx:int, dy:int):
    obj.move(obj.x() + dx, obj.y() + dy)

class myAddTask(QWidget):
    def __init__(self, parent, ser:mySerial):
        super().__init__(parent)
        self.serial = ser
        self.editAddr = myEditLine(self, self.serial, 'addr')
        self.comboOperation = myComboBox(self, self.serial, 'operation')
        self.editDataAddr = myEditLine(self, self.serial, 'dataAddr')
        self.editDataLen = myEditLine(self, self.serial, 'dataLen')
        self.comboDataType = myComboBox(self, self.serial, 'dataType')
        self.editFactory = myEditLine(self, self.serial, 'factory')
        self.editBase = myEditLine(self, self.serial, 'base')
        self.comboSbdType = myComboBox(self, self.serial, 'sbdType')
        self.editSensorType = myEditLine(self, self.serial, 'sensorType')
        self.btnAddTask = myButton(self, self.serial, 'add')
        self.btnDelTask = myButton(self, self.serial, 'del')
        self.editIndex = myEditLine(self, self.serial, 'index')
        self.initUI()

    def initUI(self):
        self.editAddr.label.setText('设备地址:')
        self.editAddr.move(40, 0)
        relativeMove(self.editAddr.lineEdit, -35, 0)
        self.editAddr.lineEdit.setText('1')

        self.comboOperation.label.setText('MODBUS操作码:')
        self.comboOperation.combo.addItem('3')
        self.comboOperation.combo.addItem('4')
        self.comboOperation.move(260, 0)
        relativeMove(self.comboOperation.combo, 0, 5)
        self.comboOperation.combo.setCurrentIndex(0)

        self.editDataAddr.label.setText('数据地址:')
        self.editDataAddr.move(480, 0)
        relativeMove(self.editDataAddr.lineEdit, -30, 0)
        self.editDataAddr.lineEdit.setText('20000')

        self.editDataLen.label.setText('数据长度:')
        self.editDataLen.move(700, 0)
        relativeMove(self.editDataLen.lineEdit, -30, 0)
        self.editDataLen.lineEdit.setText('1')

        dataType = ['U16']
        self.comboDataType.label.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.comboDataType.label.setText('数据类型:')
        for dt in dataType:
            self.comboDataType.combo.addItem(dt)
        self.comboDataType.move(40, 40)
        relativeMove(self.comboDataType.combo, -30, 5)

        self.editFactory.label.setText('系数:')
        self.editFactory.move(260, 40)
        relativeMove(self.editFactory.lineEdit, -60, 0)
        self.editFactory.lineEdit.setText('0.1')

        self.editBase.label.setText('基数:')
        self.editBase.move(480, 40)
        relativeMove(self.editBase.lineEdit, -60, 0)
        self.editBase.lineEdit.setText('0')

        self.comboSbdType.label.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.comboSbdType.label.resize(120, 30)
        self.comboSbdType.label.setText('输变电数据类型:')
        self.comboSbdType.combo.addItem('FLOAT')
        self.comboSbdType.combo.addItem('INT')
        self.comboSbdType.combo.addItem('UINT')
        self.comboSbdType.combo.addItem('SWITCH')
        self.comboSbdType.move(700, 80)
        relativeMove(self.comboSbdType.combo, 10, 5)
        self.comboSbdType.combo.setCurrentIndex(0)

        self.editSensorType.label.setText('传感器类型值:')
        self.editSensorType.move(700, 40)
        relativeMove(self.editSensorType.lineEdit, -5, 0)
        self.editSensorType.lineEdit.setText('2054')

        self.editIndex.label.setText('指令序号:')
        self.editIndex.move(40, 80)
        relativeMove(self.editIndex.lineEdit, -30, 0)
        self.editIndex.lineEdit.setText('1')

        self.btnAddTask.setGeometry(40, 120, 120, 40)
        self.btnAddTask.clicked[bool].connect(self.sendAddCmd)

        self.btnDelTask.setGeometry(170, 120, 120, 40)
        self.btnDelTask.clicked[bool].connect(self.sendDelCmd)

    def sendAddCmd(self):
        cmd = 'set,cmd,'+f'{self.editIndex.lineEdit.text()}'+','+f'{self.editAddr.lineEdit.text()}'+','+f'{self.comboOperation.combo.currentText()}'+','
        cmd += f'{self.editDataAddr.lineEdit.text()}'+','+f'{self.editDataLen.lineEdit.text()}'+','
        cmd += f'{self.comboDataType.combo.currentText()}'+','+f'{self.editFactory.lineEdit.text()}'+','
        cmd += f'{self.editBase.lineEdit.text()}'+','+f'{self.comboSbdType.combo.currentText()}'+','+f'{self.editSensorType.lineEdit.text()}'
        if self.serial.is_open:
            while len(cmd) > 32:
                self.serial.write(cmd[0:32].encode())
                time.sleep(1.5)
                cmd = cmd[32:]
                #print(cmd)

            if len(cmd) > 0:
                self.serial.write(cmd.encode())

    def sendDelCmd(self):
        cmd = 'delete cmd,'+f'{self.editIndex.lineEdit.text()}'
        if self.serial.is_open:
            while len(cmd) > 32:
                self.serial.write(cmd[0:32].encode())
                time.sleep(1.5)
                cmd = cmd[32:]
                #print(cmd)

            if len(cmd) > 0:
                self.serial.write(cmd.encode())
