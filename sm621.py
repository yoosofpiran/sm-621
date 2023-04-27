import sys
import serial
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        self.ser = None

    def initUI(self):
        self.portLabel = QLabel("Serial Port:")
        self.portComboBox = QComboBox()
        self.baudrateLabel = QLabel("Baudrate:")
        self.baudrateComboBox = QComboBox()
        self.sendButton = QPushButton("Send Command")
        self.openButton = QPushButton("Open Port")
        self.closeButton = QPushButton("Close Port")
        self.receiveTextEdit = QTextEdit()

        # add items to port and baudrate comboboxes
        self.portComboBox.addItems(["COM11", "COM2", "COM3"])
        self.baudrateComboBox.addItems(["9600", "19200", "38400", "57600", "115200"])

        # set layout
        mainLayout = QVBoxLayout()
        portLayout = QHBoxLayout()
        baudrateLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        portLayout.addWidget(self.portLabel)
        portLayout.addWidget(self.portComboBox)
        baudrateLayout.addWidget(self.baudrateLabel)
        baudrateLayout.addWidget(self.baudrateComboBox)
        buttonLayout.addWidget(self.sendButton)
        buttonLayout.addWidget(self.openButton)
        buttonLayout.addWidget(self.closeButton)

        mainLayout.addLayout(portLayout)
        mainLayout.addLayout(baudrateLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.receiveTextEdit)

        self.setLayout(mainLayout)

        # set signals and slots
        self.sendButton.clicked.connect(self.sendCommand)
        self.openButton.clicked.connect(self.openPort)
        self.closeButton.clicked.connect(self.closePort)

    def sendCommand(self):
        if self.ser is None or not self.ser.is_open:
            self.receiveTextEdit.append("Error: Serial port is not open.")
            return
        
        cmd = bytearray.fromhex("c0 01 00 00 00 00 00 05 14 00 00 00 00 00 00 c0")
        checksum = sum(cmd) & 0xffff
        checksum_bytes = checksum.to_bytes(2, byteorder="little")
        cmd[-3:-1] = checksum_bytes
        self.ser.write(cmd)
        self.receiveResponse()

    def receiveResponse(self):
        response = bytearray(self.ser.read_until(b"\xc0"))
        while len(response) < 13 or response[0] != 0xc0 or response[-1] != 0xc0:
            response += self.ser.read_until(b"\xc0")
        response_checksum = sum(response[1:11]) & 0xffff
        response_checksum_bytes = response[-3:-1]
        expected_checksum_bytes = response_checksum.to_bytes(2, byteorder="little")
        if response_checksum_bytes != expected_checksum_bytes:
            self.receiveTextEdit.append("Error: Invalid response checksum.")
        else:
            if response[1] == 0x00:
                self.receiveTextEdit.append("Command sent successfully.")
            else:
                self.receiveTextEdit.append("Error: Command failed with response code: {}".format(response[1]))
                
    
    def openPort(self):
          if self.ser is not None and self.ser.is_open:
              self.receiveTextEdit.append("Error: Serial port is already open.")
              return
    
          port = self.portComboBox.currentText()
          baudrate = int(self.baudrateComboBox.currentText())
    
          try:
              self.ser = serial.Serial(port, baudrate, timeout=0.5)
              self.receiveTextEdit.append("Serial port opened successfully.")
          except Exception as e:
              self.ser = None
              self.receiveTextEdit.append("Error: Could not open serial port: {}".format(str(e)))

    def closePort(self):
          if self.ser is None or not self.ser.is_open:
              self.receiveTextEdit.append("Error: Serial port is not open.")
              return
    
          try:
             self.ser.close()
             self.receiveTextEdit.append("Serial port closed successfully.")
          except Exception as e:
            self.receiveTextEdit.append("Error: Could not close serial port: {}".format(str(e)))
          finally:
           self.ser = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
