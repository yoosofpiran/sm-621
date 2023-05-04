import time
from adafruit_fingerprint import Adafruit_Fingerprint

# ایجاد شیء Adafruit_Fingerprint
f = Adafruit_Fingerprint()

# باز کردن پورت سریال
#ser = serial.Serial('COM7', baudrate=57600, timeout=1.0)

# ارسال دستور "get_image"
#f.write_cmd(Adafruit_Fingerprint._VERIFYPASSWORD)
f.get_image()
# دریافت پاسخ
#response = f.read_packet(UART)

# بستن پورت سریال
#ser.close()

# چاپ پاسخ دریافتی
#print(response)
