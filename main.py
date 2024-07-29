# 导入类
import sys

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QApplication, QTextEdit, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtGui

import serial, time
import serial.tools.list_ports

from sbdSerial import mySerial
from sdbWidget import myComboBox, myButton, myAddTask, myEditLineWithButton

class SerialReadThread(QThread):
    def __init__(self, ser:mySerial):
        super(SerialReadThread, self).__init__()
        self.serial = ser

    def run(self):
        ser = self.serial
        while True:
            if ser.is_open:
                if ser.readFlag and ser.in_waiting > 0:
                    data = ser.readline()
                    try:
                        utf8_data = data.decode('utf-8')  # 读取一行数据，解码为字符串
                        ser.input.setReadOnly(False)
                        ser.input.insertPlainText(utf8_data)
                        ser.input.setReadOnly(True)
                        ser.input.moveCursor(QtGui.QTextCursor.MoveOperation.End)
                    except UnicodeDecodeError:
                        print(f'{data.count}')
                        pass
                time.sleep(0.1)  # 等待一段时间继续读取
            time.sleep(0.5)

class RefreshPortThread(QThread):
    def __init__(self, port_combo:myComboBox):
        super(RefreshPortThread, self).__init__()
        self.combo = port_combo

    def run(self):
        portCombo = self.combo
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
            
if __name__ == '__main__':
    # 创建 QApplication 类的实例，并传入命令行参数
    app = QApplication(sys.argv)

    desktop = QDesktopWidget()
    screen_width = desktop.screenGeometry().width()
    screen_height = desktop.screenGeometry().height()

    window_width = 920   #screen_width/2
    window_height = 1020 #screen_height/2

    # 创建 QWidget 类的实例，相当于创建一个窗口
    w = QWidget()
    # 设置宽高位置
    w.setGeometry(int(screen_width/2) - int(window_width/2), int(screen_height/2) - int(window_height/2), int(window_width), int(window_height))

    input =  QTextEdit(w)
    input.setGeometry(40, 290, 400, 400)
    input.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    input.setReadOnly(True)

    output =  QTextEdit(w)
    output.setGeometry(450, 290, 400, 400)
    output.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    ser = mySerial(input, output, 0.5)

    QToolTip.setFont(QFont('SansSerif', 10))
    btn1 = myButton(w, ser, 'start_stop')
    btn1.setGeometry(40, 40, 80, 40)

    btn2 = myButton(w, ser, 'send')
    btn2.setGeometry(450, 700, 80, 40)

    btn3 = myButton(w, ser, 'ATsend')
    btn3.setGeometry(550, 700, 100, 40)

    btn4 = myButton(w, ser, 'clear')
    btn4.setGeometry(40, 700, 80, 40)

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
    portCombo.combo.resize(portCombo.combo.width(), 25)
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

    btn5 = myButton(w, ser, 'TouChuan1')
    btn5.move(40, 760)

    btn6 = myButton(w, ser, 'TouChuan2')
    btn6.move(40, 800)

    setCycle = myEditLineWithButton(w, ser, 'setCycle')
    setCycle.move(270, 760)

    setAddr = myEditLineWithButton(w, ser, 'setAddr')
    setAddr.move(270, 800)

    setChn = myEditLineWithButton(w, ser, 'setChn')
    setChn.move(580, 760)

    addTask = myAddTask(w, ser)
    addTask.move(0, 850)

    btn7 = myButton(w, ser, 'reboot')
    btn7.move(800, 980)

    # 设置窗口的标题与图标
    w.setWindowTitle('输变电配置')
    app.setWindowIcon(QIcon("./sbd.ico"))

    readSerial = SerialReadThread(ser)
    readSerial.start()

    port_refresh_thread = RefreshPortThread(portCombo)
    port_refresh_thread.start()

    # 显示窗口
    w.show()
    # 进入程序主循环，并通过 exit 确保主循环安全结束
    sys.exit(app.exec_())
