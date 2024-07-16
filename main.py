# 导入类
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QApplication, QLineEdit, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont

import serial, threading, time
import serial.tools.list_ports

from sbdSerial import mySerial
from sdbWidget import myComboBox, myButton, myEditLine

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

def check_ports():
    before = {p.device for p in serial.tools.list_ports.comports()}
    while True:
        time.sleep(1)  # 每秒检查一次
        after = {p.device for p in serial.tools.list_ports.comports()}
        
        added = after - before
        removed = before - after
        
        if added:
            print(f"Added: {', '.join(added)}")
        if removed:
            print(f"Removed: {', '.join(removed)}")
        
        before = after

def serial_port_refresh(port_combo:myComboBox):
    before = {p.device for p in serial.tools.list_ports.comports()}
    while True:
        time.sleep(1)  # 每秒检查一次
        after = {p.device for p in serial.tools.list_ports.comports()}
        
        added = after - before
        removed = before - after
        
        if added or removed:
            portCombo.combo.clear()
            portCombo.combaItemNumber = 0
            ports = serial.tools.list_ports.comports()
            for port in ports:
                portCombo.combo.addItem(f"{port.device}")
                portCombo.combaItemNumber += 1
        
        before = after

def relativeMove(obj, dx:int, dy:int):
    obj.move(obj.x() + dx, obj.y() + dy)

if __name__ == '__main__':
    # 创建 QApplication 类的实例，并传入命令行参数
    app = QApplication(sys.argv)

    desktop = QDesktopWidget()
    screen_width = desktop.screenGeometry().width()
    screen_height = desktop.screenGeometry().height()
    #print(f"Screen Width: {screen_width}")
    #print(f"Screen Height: {screen_height}")

    window_width = 960
    window_height = 950

    # 创建 QWidget 类的实例，相当于创建一个窗口
    w = QWidget()
    # 设置宽高位置
    w.setGeometry(int(screen_width/2) - int(window_width/2), int(screen_height/2) - int(window_height/2), window_width, window_height)

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
        portCombo.combaItemNumber += 1
    else:
        for port in ports:
            portCombo.combo.addItem(f"{port.device}")
            portCombo.combaItemNumber += 1
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

    editAddr = myEditLine(w, ser, 'addr')
    editAddr.label.setText('设备地址:')
    editAddr.move(40, 750)
    relativeMove(editAddr.lineEdit, -35, 0)
    editAddr.lineEdit.setText('1')

    comboOperation = myComboBox(w, ser, 'operation')
    comboOperation.label.setText('MODBUS操作码:')
    comboOperation.combo.addItem('3')
    comboOperation.combo.addItem('4')
    comboOperation.move(260, 750)
    relativeMove(comboOperation.combo, 0, 5)
    comboOperation.combo.setCurrentIndex(0)

    editDataAddr = myEditLine(w, ser, 'dataAddr')
    editDataAddr.label.setText('数据地址:')
    editDataAddr.move(480, 750)
    relativeMove(editDataAddr.lineEdit, -30, 0)
    editDataAddr.lineEdit.setText('20000')

    editDataLen = myEditLine(w, ser, 'dataLen')
    editDataLen.label.setText('数据长度:')
    editDataLen.move(700, 750)
    relativeMove(editDataLen.lineEdit, -30, 0)
    editDataLen.lineEdit.setText('1')

    comboDataType = myComboBox(w, ser, 'dataType')
    comboDataType.label.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
    comboDataType.label.setText('数据类型:')
    comboDataType.combo.addItem('U16')
    comboDataType.move(40, 790)
    relativeMove(comboDataType.combo, -30, 5)

    editFactory = myEditLine(w, ser, 'factory')
    editFactory.label.setText('系数:')
    editFactory.move(260, 790)
    relativeMove(editFactory.lineEdit, -60, 0)
    editFactory.lineEdit.setText('0.1')

    editBase = myEditLine(w, ser, 'base')
    editBase.label.setText('基数:')
    editBase.move(480, 790)
    relativeMove(editBase.lineEdit, -60, 0)
    editBase.lineEdit.setText('0')

    comboSbdType = myComboBox(w, ser, 'sbdType')
    comboSbdType.label.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
    comboSbdType.label.resize(120, 30)
    comboSbdType.label.setText('输变电数据类型:')
    comboSbdType.combo.addItem('FLOAT')
    comboSbdType.combo.addItem('INT')
    comboSbdType.combo.addItem('UINT')
    comboSbdType.combo.addItem('SWITCH')
    comboSbdType.move(700, 830)
    relativeMove(comboSbdType.combo, 10, 5)
    comboSbdType.combo.setCurrentIndex(0)

    editSensorType = myEditLine(w, ser, 'sensorType')
    editSensorType.label.setText('传感器类型值:')
    editSensorType.move(700, 790)
    relativeMove(editSensorType.lineEdit, -5, 0)
    editSensorType.lineEdit.setText('2054')

    btn3 = myButton(w, ser, 'add')
    btn3.setGeometry(700, 870, 120, 40)

    # 设置窗口的标题与图标
    w.setWindowTitle('输变电配置')
    app.setWindowIcon(QIcon("./sbd.ico"))

    read_thread = threading.Thread(target=read_serial, args=(ser,))
    read_thread.start()

    port_refresh_thread = threading.Thread(target=serial_port_refresh, args=(portCombo,))
    port_refresh_thread.start()

    # 显示窗口
    w.show()
    # 进入程序主循环，并通过 exit 确保主循环安全结束
    sys.exit(app.exec_())
