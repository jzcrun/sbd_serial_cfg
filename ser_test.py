import time
import serial
import serial.tools.list_ports

def start_serial(com:str, baud:int, data_bit:int = 8, parity:str = "N", stop_bit:float = 1) -> None:
    # 打开串口，这里的'COM3'是串口号，根据电脑情况进行修改
    ser = serial.Serial(com, baud, data_bit, parity, stop_bit)
    # 检查串口是否正确打开
    if ser.is_open:
        print("串口已打开")
    else:
        print("无法打开串口")

    # 读取数据
    # 这里的timeout指的是读取操作的超时时间，单位是秒
    # 如果在指定时间内没有接收到数据，则会抛出serial.SerialException异常
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8')  # 读取一行数据，解码为字符串
                print(data)  # 打印读取到的数据
            time.sleep(0.5)  # 等待一段时间继续读取

    except serial.SerialException:
        print("读取数据时发生错误")

    # 关闭串口
    ser.close()

if __name__ == '__main__':
    ports = serial.tools.list_ports.comports()
    # 打印每个可用串口的名称
    print("Available ports:")
    for port in ports:
        print(f"{port}: {port.device}")
    start_serial('COM11', 115200)
