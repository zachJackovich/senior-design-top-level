from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from time import sleep
from gpiozero import DistanceSensor
from threading import Thread

message = ""
reading = True
lcd = LCD()
sensor = DistanceSensor(echo = 20, trigger = 21)

def safe_exit(signum, frame):
    exit(1)

def display_distance():
    global message
    
    while reading:
        sleep(0.25)
        lcd.text(message, 1)

def read_distance():
    global message
    
    while reading:
        message = "Distance: " + '{:1.2f}'.format(sensor.value) + " m"
        
        print(message)
        sleep(0.1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

try:
    reader = Thread(target=read_distance, daemon=True)
    display = Thread(target=display_distance, daemon=True)
    
    reader.start()
    display.start()
    
    pause()

except KeyboardInterrupt:
    pass

finally:
    reading = False
    sleep(0.5)
    lcd.clear()
    sensor.close()