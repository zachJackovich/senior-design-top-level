import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#Set GPIO Pin 21 as Input, and set an internal Pull-Down Resistor 
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    print("Starting GPIO Test from MSP430 to RPi...")
    while True:
        if(GPIO.input(16)):
            print("GPIO is High")
        else:
            print("GPIO is Low")
        time.sleep(1)
            
finally:
    print("Exiting GPIO Test...")
    GPIO.cleanup()
