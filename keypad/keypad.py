import RPi.GPIO as GPIO
import I2C_LCD_driver
import time

L1 = 26
L2 = 13
L3 = 25
L4 = 24
C1 = 23
C2 = 22
C3 = 27
C4 = 17

#initialize LCD object
lcd = I2C_LCD_driver.lcd()
lcd.lcd_clear()

#Setup the GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

string = ""

#creating the function definiton for readLine() that takes the line # and characters on that line as arguments
def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        print(characters[0])
        string = string + characters[0]
        lcd.lcd_display_string(characters[0], 1, 0)
    if(GPIO.input(C2) == 1):
        print(characters[1])
        string = string + characters[1]
        lcd.lcd_display_string(characters[1], 1, 0)
    if(GPIO.input(C3) == 1):
        print(characters[2])
        string = string + characters[2]
        lcd.lcd_display_string(characters[2], 1, 0)
    if(GPIO.input(C4) == 1):
        print(characters[3])
        string = string + characters[3]
        lcd.lcd_display_string(characters[3], 1, 0)
    GPIO.output(line, GPIO.LOW)

try:
    while True:
        readLine(L1, ["1","2","3","A"])
        readLine(L2, ["4","5","6","B"])
        readLine(L3, ["7","8","9","C"])
        readLine(L4, ["*","0","#","D"])
        time.sleep(0.1)
    
except KeyboardInterrupt:
    print("\nApplication stopped!")
    print("Pin Number Detected: " + string)
    lcd.lcd_clear()

