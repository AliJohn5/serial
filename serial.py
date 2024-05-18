# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget,QPushButton, QGridLayout, QLabel,QLineEdit,QVBoxLayout,QHBoxLayout,QTextBrowser
from PySide6.QtCore import Qt,QTimer
import serial
import time

class MySerial():
    def __init__(self, serial_port, baud_rate, wd):
        super().__init__()
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.wd = wd
        self.serial = None
        self.timer = None
        self.isSend = False
        self.open_serial()


    def open_serial(self):
        try:
            self.serial = serial.Serial(self.serial_port,int( self.baud_rate) )

            timer_period = 10
            self.timer = QTimer()
            self.timer.timeout.connect(self.timer_callback)
            self.timer.start(timer_period)
            self.wd.textbrowser.append("OK Serial is Ready")

        except serial.SerialException as e:
            if(e.errno == 13):
                self.wd.textbrowser.append(" [Errno 13] could not open port /dev/ttyACM0: [Errno 13] Permission denied: '/dev/ttyACM0',you can fix it by Run: sudo python3 <your file>\n, or Change the permissions of the device file:\n sudo chmod 666 "+ self.serial_port)

            self.wd.textbrowser.append(f"Error opening serial port: {e}")

    def timer_callback(self):
        if(self.isSend):
            return

        by = self.serial.in_waiting

        if by > 0:
            data = self.serial.read(by).decode("utf-8")
            self.wd.textbrowser.append("receiving: " + data)


    def send_data(self,data):
        self.isSend = True
        try:
            self.wd.textbrowser.append("sending: " + data)
            self.serial.write(data.encode())
            time.sleep(0.05)
        except serial.SerialException as e:
            self.wd.textbrowser.append(f"Error sending: {e}")
            self.wd.lineCMD.clear()
            return
        self.isSend = False
        self.wd.textbrowser.append("done")
        self.wd.lineCMD.clear()



    def close_serial(self):
        if self.serial is not None and self.serial.is_open:
            self.serial.close()
            if self.timer is not None:
                self.timer.stop()
        self.wd.textbrowser.append("Serial is closed ")


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.ser = None
        self.baud_line = QLineEdit("",self)
        self.baud_line.setFixedWidth(200)

        self.rate_line = QLineEdit("",self)
        self.lineCMD = QLineEdit("",self)

        self.rate_line.setFixedWidth(200)

        self.textbrowser = QTextBrowser()


        button1 = QPushButton("switch serial on", self)
        button2 = QPushButton("switch serial off", self)

        button_height = 75
        #button_width = 400

        button_style = """
            QPushButton {
                background-color: #777777;
                color: white;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
        """



        for button in [button1, button2]:
            button.setFixedHeight(button_height)
           # button.setFixedWidth(button_width)
            button.setStyleSheet(button_style)


        #self.label = QLabel("Press a button", self)
        self.labelName = QLabel("Port Name:", self)
        self.labelRate = QLabel("Port Rate:", self)


        self.labelCMD = QLabel("MSG:", self)

        #self.label.setAlignment(Qt.AlignCenter)
        self.labelName.setAlignment(Qt.AlignLeft)
        self.labelRate.setAlignment(Qt.AlignLeft)

        self.labelName.setFixedWidth(100)
        self.labelRate.setFixedWidth(100)
        self.labelCMD.setFixedWidth(70)
        self.labelCMD.setFixedHeight(40)



        self.textbrowser.setStyleSheet("""
            QTextBrowser {
                background-color: #333333;
                font-size: 18px;
                padding: 15px;
                border: 1px solid #d3d3d3;
                border-radius: 10px;
            }
        """)


        self.lineCMD.setPlaceholderText("Type something and press Enter to send")
        self.lineCMD.editingFinished.connect(self.on_editing_finished)







        button1.clicked.connect(self.on_button1_clicked)
        button2.clicked.connect(self.on_button2_clicked)



        self.labelName.setStyleSheet("""
        QLabel {
            background-color: #333333;
            font-size: 12px;
            padding: 10px;
            border: 1px solid #d3d3d3;
            border-radius: 4px;
        }
        """
        )

        self.labelCMD.setStyleSheet("""
        QLabel {
            background-color: #333333;
            font-size: 12px;
            padding: 10px;
            border: 1px solid #d3d3d3;
            border-radius: 4px;

        }
        """
        )

        self.labelRate.setStyleSheet("""
        QLabel {
            background-color: #333333;
            font-size: 12px;
            padding: 10px;

            border: 1px solid #d3d3d3;
            border-radius: 4px;
        }
        """
        )

        self.baud_line.setStyleSheet("""
        QLineEdit {
            background-color: #333333;
            font-size: 12px;
            padding: 2px;
            border: 1px solid #d3d3d3;
            border-radius: 4px;
        }
        """
        )

        self.rate_line.setStyleSheet("""
        QLineEdit {
            background-color: #333333;
            font-size: 12px;
            padding: 2px;
            border: 1px solid #d3d3d3;
            border-radius: 4px;
        }
        """
        )

        self.lineCMD.setStyleSheet("""
        QLineEdit {
            background-color: #333333;
            font-size: 12px;
            padding: 2px;
            border: 1px solid #d3d3d3;
            border-radius: 4px;
        }
        """
        )






        self.layout = QGridLayout(self)


        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        h3.setSpacing(10)
        hl = QVBoxLayout()

        h3.addWidget(self.labelCMD)
        h3.addWidget(self.lineCMD)



        h1.setAlignment(Qt.AlignCenter)
        h2.setAlignment(Qt.AlignCenter)

        #hl.setAlignment(Qt.AlignCenter)

        h1.addWidget(self.labelName)
        h1.addWidget(self.baud_line)

        h2.addWidget(self.labelRate)
        h2.addWidget(self.rate_line)

        hl.addLayout(h1)
        hl.addLayout(h2)

        h1.setSpacing(5)
        h2.setSpacing(5)
        hl.setSpacing(5)




        self.layout.addWidget(self.textbrowser, 0, 0, 2, 4)
        self.layout.addLayout(h3,2,0,1,0)

        self.layout.addWidget(button1, 3, 0,1,2)
        self.layout.addWidget(button2, 4, 0,1,2)

        self.layout.addLayout(hl,3,2,1,2)




        self.setLayout(self.layout)
        self.setWindowTitle('Serila Communication')
        self.resize(800, 600)

    def on_button1_clicked(self):
        if(self.baud_line.text()=="" or self.rate_line.text()==""):
            self.textbrowser.append("please enter Serial port Name and Rate")
            return
        self.ser = MySerial(self.baud_line.text(),self.rate_line.text(),self)


    def on_button2_clicked(self):
        if (self.ser is not None):
            self.ser.close_serial()

    def on_editing_finished(self):
        if (self.ser is not None):
            self.ser.send_data(self.lineCMD.text())
        else:
            self.textbrowser.append("please switch serial on")





if __name__ == "__main__":
    app = QApplication([])
    window = Widget()
    window.show()
    sys.exit(app.exec())
