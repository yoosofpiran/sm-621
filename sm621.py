import serial
import threading
import tkinter as tk
from tkinter import ttk

class SM621GUI:
    def __init__(self, master):
        self.master = master
        master.title("SM621 Serial Reader")

        # Create Serial Port Label and Combo Box
        self.serial_port_label = ttk.Label(master, text="Serial Port:")
        self.serial_port_label.grid(column=0, row=0, padx=5, pady=5)

        self.serial_port_combo = ttk.Combobox(master, values=self.serial_ports())
        self.serial_port_combo.grid(column=1, row=0, padx=5, pady=5)
        self.serial_port_combo.current(0)

        # Create Baud Rate Label and Combo Box
        self.baud_rate_label = ttk.Label(master, text="Baud Rate:")
        self.baud_rate_label.grid(column=0, row=1, padx=5, pady=5)

        self.baud_rate_combo = ttk.Combobox(master, values=["2400", "4800", "9600", "19200", "38400", "57600", "115200"])
        self.baud_rate_combo.grid(column=1, row=1, padx=5, pady=5)
        self.baud_rate_combo.current(2)

        # Create Open and Close Serial Port Buttons
        self.open_button = ttk.Button(master, text="Open Port", command=self.open_serial_port)
        self.open_button.grid(column=0, row=2, padx=5, pady=5)

        self.close_button = ttk.Button(master, text="Close Port", command=self.close_serial_port, state="disabled")
        self.close_button.grid(column=1, row=2, padx=5, pady=5)

        # Create Send Command Button
        self.send_command_button = ttk.Button(master, text="Send Command", command=self.send_command, state="disabled")
        self.send_command_button.grid(column=2, row=2, padx=5, pady=5)

        # Create Text Box to Display Received Data
        self.text_box = tk.Text(master, width=50, height=10)
        self.text_box.grid(column=0, row=3, columnspan=3, padx=5, pady=5)

        # Set up serial port object
        self.ser = None
        self.ser_lock = threading.Lock()

        # Set up thread for reading serial data
        self.thread = threading.Thread(target=self.serial_reader_thread)
        self.thread_stop_event = threading.Event()

    def serial_ports(self):
        """ Lists serial port names """
        ports = ['COM{}'.format(i + 1) for i in range(256)]
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def open_serial_port(self):
        """ Opens the selected serial port """
        port = self.serial_port_combo.get()
        baud_rate = self.baud_rate_combo.get()

        if not self.ser:
            try:
                self.ser = serial.Serial(port, baud_rate)
                self.open_button.config(state="disabled")
                self.close_button.config(state="enabled")
                self.send_command_button.config(state="enabled")
                self.thread_stop_event.clear()
                self.thread.start()
            except serial.SerialException as e:
                self.text_box.insert(tk.END, "Error opening serial port: {}\n".format(str(e)))
        else:
            self
