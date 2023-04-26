import sys
import serial
from serial.tools import list_ports
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QTextEdit, QMessageBox, QLabel
from PyQt5.QtCore import QThread, pyqtSignal


class SerialThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port, baudrate, parent=None):
        super().__init__(parent)
        self.port = port
        self.baudrate = baudrate
        self.serial_port = None

    def run(self):
        try:
            self.serial_port = serial.Serial(self.port, self.baudrate)
            while self.serial_port.isOpen():
                data = self.serial_port.read_until(b'\xc0').decode('utf-8', errors='ignore')
                self.data_received.emit(data)
        except Exception as e:
            print(e)
            self.serial_port.close()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Serial Port Reader')
        self.setGeometry(100, 100, 500, 500)

        self.serial_thread = None

        self.com_label = QLabel('COM Port:', self)
        self.com_label.setGeometry(20, 20, 100, 30)

        self.com_combo = QComboBox(self)
        self.com_combo.setGeometry(120, 20, 150, 30)

        self.refresh_button = QPushButton('Refresh', self)
        self.refresh_button.setGeometry(280, 20, 100, 30)
        self.refresh_button.clicked.connect(self.refresh_ports)

        self.baud_label = QLabel('Baudrate:', self)
        self.baud_label.setGeometry(20, 60, 100, 30)

        self.baud_combo = QComboBox(self)
        self.baud_combo.setGeometry(120, 60, 150, 30)
        self.baud_combo.addItems(['9600', '19200', '38400', '57600', '115200'])

        self.open_button = QPushButton('Open', self)
        self.open_button.setGeometry(280, 60, 100, 30)
        self.open_button.clicked.connect(self.open_port)

        self.close_button = QPushButton('Close', self)
        self.close_button.setGeometry(390, 60, 100, 30)
        self.close_button.clicked.connect(self.close_port)
        self.close_button.setEnabled(False)

        self.send_button = QPushButton('Send', self)
        self.send_button.setGeometry(20, 100, 100, 30)
        self.send_button.clicked.connect(self.send_command)

        self.command_text = QTextEdit(self)
        self.command_text.setGeometry(130, 100, 360, 30)

        self.receive_text = QTextEdit(self)
        self.receive_text.setGeometry(20, 140, 470, 300)
        self.receive_text.setReadOnly(True)

    def refresh_ports(self):
        self.com_combo.clear()
        ports = list_ports.comports()
        for port in ports:
            self.com_combo.addItem(port.device)

    def open_port(self):
        port = self.com_combo.currentText()
        baudrate = int(self.baud_combo.currentText())
        self.serial_thread = SerialThread(port, baudrate, self)
        self.serial_thread.data_received.connect(self.receive_data)
        self.serial_thread.start()
        self.open_button.setEnabled(False)
        self.close_button.setEnabled(True)

    def close_port(self):
        self.serial_thread.terminate()
        self.serial_thread.wait()
        self.serial_thread = None
        self.open_button.setEnabled(True)
        self.close_button.setEnabled(False)

def send_command(self):
    # Disable the close button and enable the send button
    self.close_button.setEnabled(False)
    self.send_button.setEnabled(True)

    # Get the selected baud rate
    baud_rate = int(self.baud_rate_combobox.currentText())

    # Get the selected COM port
    com_port = self.com_port_combobox.currentText()

    try:
        # Open the serial port
        self.serial_port = serial.Serial(com_port, baud_rate, timeout=1)

        # Convert the command to bytes
        command = bytes([0xc0, 0x01, 0xff, 0xff, 0xff, 0xff])

        # Send the command
        self.serial_port.write(command)

        # Wait for the response
        response = self.serial_port.read_until(bytes([0xc0]))

        # Display the response
        self.receive_textbox.setText(response.hex())

    except serial.serialutil.SerialException:
        # Display an error message if the port could not be opened
        QMessageBox.critical(self, "Error", "Could not open serial port.")

    finally:
        # Close the serial port and re-enable the close button
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.close()
        self.close_button.setEnabled(True)
