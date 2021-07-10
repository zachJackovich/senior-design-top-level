from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time

lcd = LCD()

def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

try:
    while(True):
        lcd.text("Hello,", 1)
        lcd.text("Raspberry Pi!", 2)
        time.sleep(3)
        lcd.clear()
        lcd.text("It's time...", 1)
        lcd.text("to get to work!", 2)
        time.sleep(3)
        lcd.clear()

except KeyboardInterrupt:
    pass

finally:
    lcd.clear()

