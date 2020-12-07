"""
 @Author       :linyu
 @File         :com_engine.py
 @Description  :
 @Software     :PyCharm
"""

import serial


class SerialCommunication:
    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        global RET
        self.main_engine = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

    def print_name(self):
        print(self.main_engine.name)
        print(self.main_engine.port)
        print(self.main_engine.baudrate)
        print(self.main_engine.bytesize)
        print(self.main_engine.parity)
        print(self.main_engine.stopbits)
        print(self.main_engine.timeout)
        print(self.main_engine.writeTimeout)
        print(self.main_engine.xonxoff)
        print(self.main_engine.rtscts)
        print(self.main_engine.dsrdtr)
        print(self.main_engine.interCharTimeout)

    def open_engine(self):
        try:
            if (self.main_engine.isOpen()):
                RET = True
                print("串口打开成功")
        except Exception as exc:
            print("串口打开失败", exc)

    def close_engine(self):
        try:
            self.main_engine.close()
            if self.main_engine.isOpen():
                print("串口未关闭")
            else:
                print("串口已关闭")
        except Exception as exc:
            print("关闭异常", exc)

    def read_size(self, size):
        return self.main_engine.read(size=size)

    def read_line(self):
        return self.main_engine.readline()

    def send_data(self, data):
        try:
            self.main_engine.write(data.encode("gbk"))
            print("已发送数据：", data)
        except Exception as exc:
            print("发送异常", exc)

    def recive_data(self, way=1):
        while True:
            try:
                if self.main_engine.in_waiting:
                    if (way == 0):
                        for i in range(self.main_engine.in_waiting):
                            print("接收ascii数据：", str(self.read_size(1)))
                            data1 = self.read_size(1).hex()
                            data2 = int(data1, 16)
                            print("收到数据十六进制：", data1)
                            print("收到数据十进制：", data2)
                    if (way == 1):
                        data = self.main_engine.read_all()
                        print("整体接收：", data)
            except Exception as exc:
                print("接收异常：", exc)


if __name__ == '__main__':
    data = "*fm800p-100sE"
    communication = SerialCommunication('COM19', 9600, 0.5)
    communication.open_engine()
    communication.send_data(data)
    communication.close_engine()

    communication_reciver = SerialCommunication('COM23', 9600, 0.5)
    communication_reciver.open_engine()
    communication_reciver.recive_data()
    communication_reciver.close_engine()
