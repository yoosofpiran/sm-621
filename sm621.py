import serial
import threading
import tkinter as tk
from tkinter import ttk

class SerialGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Serial GUI")

        # Initialize serial port
        self.ser = None

        # Initialize GUI elements
        self.port_label = ttk.Label(master, text="Port:")
        self.port_label.grid(row=0, column=0)

        self.port_entry = ttk.Entry(master)
        self.port_entry.grid(row=0, column=1)

        self.baudrate_label = ttk.Label(master, text="Baudrate:")
        self.baudrate_label.grid(row=1, column=0)

        self.baudrate_entry = ttk.Entry(master)
        self.baudrate_entry.insert(0, "9600")
        self.baudrate_entry.grid(row=1, column=1)

        self.open_button = ttk.Button(master, text="Open", command=self.open_port)
        self.open_button.grid(row=2, column=0)

        self.close_button = ttk.Button(master, text="Close", command=self.close_port)
        self.close_button.grid(row=2, column=1)

        self.send_button = ttk.Button(master, text="Send", command=self.send_command)
        self.send_button.grid(row=3, column=0)

        self.receive_label = ttk.Label(master, text="Received Data:")
        self.receive_label.grid(row=4, column=0)

        self.receive_text = tk.Text(master, height=10, state="disabled")
        self.receive_text.grid(row=5, column=0, columnspan=2)

        # Initialize thread for receiving data
        self.thread = threading.Thread(target=self.receive_data, daemon=True)

    def open_port(self):
        if self.ser:
            self.ser.close()

        port = self.port_entry.get()
        baudrate = int(self.baudrate_entry.get())

        try:
            self.ser = serial.Serial(port, baudrate)
            self.thread.start()
            self.open_button.configure(state="disabled")
            self.close_button.configure(state="normal")
            self.send_button.configure(state="normal")
            self.port_entry.configure(state="disabled")
            self.baudrate_entry.configure(state="disabled")
        except serial.SerialException as e:
            tk.messagebox.showerror("Error", str(e))

    def close_port(self):
        if self.ser:
            self.ser.close()
            self.thread.join()
            self.open_button.configure(state="normal")
            self.close_button.configure(state="disabled")
            self.send_button.configure(state="disabled")
            self.port_entry.configure(state="normal")
            self.baudrate_entry.configure(state="normal")

    def send_command(self):
        if self.ser:
            command = bytes([0xc0, 0x1, 0xff, 0xff, 0xff, 0xff,0xc0])
            self.ser.write(command)

    def receive_data(self):
        while True:
            if self.ser:
                try:
                    data = self.ser.read_until(bytes([0xc0]))
                    self.receive_text.configure(state="normal")
                    self.receive_text.insert("end", data.hex() + "\n")
                    self.receive_text.configure(state="disabled")
                except serial.SerialException:
                    pass

root = tk.Tk()
app = SerialGUI(root)
root.mainloop()
