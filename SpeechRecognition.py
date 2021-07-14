import I2C_LCD_driver
import speech_recognition as sr
import RPi.GPIO as GPIO
import time
#from keyPad import *

#Things to do:
# Initialize LCD                          => Done
# Display a starting message to the user  =>
# message = "Speech or keypad"            =>
# if speech then run the speech function  =>
# if keypad then run the keypad function  =>

# Initialize LCD object
lcd = I2C_LCD_driver.lcd()
lcd.lcd_clear()

# Use:
#  lcd.lcd_display_string("Text to display", Row [either 1 or 2], Offset [usually 0]) 
#  to display something to the LCD Screen
# Use:
#  lcd.lcd_clear() to clear the LCD screen

# Declare the GPIO Number for the Keypad
L1 = 26
L2 = 13
L3 = 25
L4 = 24
C1 = 23
C2 = 22
C3 = 27
C4 = 17

# Setup GPIO Use
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# Setup the GPIO Pins
# Column input pins use pull-down resistors, Line output pins do not need resistors
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO from Pi to MSP430
#GPIO.setup(21, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

# Users pin definitions

Adam = '1234'
Moisess = '4321'
Reham = '5678'
Zach = '8765'


def speech():

    r = sr.Recognizer()
    message = 'empty'
    time_left = 10

    while (time_left != 0):

        with sr.Microphone() as source:
            
            print('Speech or Keypad?')   
            lcd.lcd_clear()
            lcd.lcd_display_string("Speech or", 1)
            lcd.lcd_display_string("Keypad?", 2)
            audio = r.listen(source)
            
            try:

                text = r.recognize_google(audio)

                #display LCD Message

                print('You said : ' + text)
                message = text
                
                if message == 'speech':
                    listen_for_pin()

                elif message == 'keypad':
                    string = ''
                    #string = keypad(string)
                    print ('\nThe pin was: ' + string)

                else:
                    print ("invalid input!!")
                
            except sr.UnknownValueError:
                print('Google Speech did not recognize audio')
            except sr.RequestError as e:
                print('Could not request results from Google Speech Recognition Service; {0}'.format(e))

        time_left = time_left - 1


def listen_for_pin():
    r = sr.Recognizer()
    message = 'empty'
    lcd.lcd_clear()
    lcd.lcd_display_string("Say your Pin...", 1)
    print("Say your Pin Number")
    user_recognized = False

    while not(user_recognized):
        with sr.Microphone() as source:
            audio = r.listen(source)
            text = r.recognize_google(audio)
            message = text

            if message == '1234':
                # Display welcome message to Adam
                print("Pin Number Detected...")
                lcd.lcd_clear()
                lcd.lcd_display_string("Welcome Home,", 1)
                lcd.lcd_display_string("Adam!", 2)
                user_recognized = True
                #GPIO.output(21, 1)                  #Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
                #time.sleep(2)                     #Hold the GPIO pin High for 2 Minutes
                break

            elif message == '4321':
                # Display welcome message to Moisess
                print("Pin Number Detected...")
                lcd.lcd_clear()
                lcd.lcd_display_string("Welcome Home,", 1)
                lcd.lcd_display_string("Moisess!", 2)
                user_recognized = True
                #GPIO.output(21, 1)                  #Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
                #time.sleep(2)                     # Hold the GPIO pin High for 2 Minutes
                break

            elif message == '5678':
                # Display welcome message to Reham
                print("Pin Number Detected...")
                lcd.lcd_clear()
                lcd.lcd_display_string("Welcome Home,", 1)
                lcd.lcd_display_string("Reham!", 2)
                user_recognized = True
                #GPIO.output(21, 1)                  #Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
                #time.sleep(2)                     #Hold the GPIO pin High for 2 Minutes
                break

            elif message == '8765':
                # Display welcome message to Zach
                print("Pin Number Detected...")
                lcd.lcd_clear()
                lcd.lcd_display_string("Welcome Home,", 1)
                lcd.lcd_display_string("Zach!", 2)
                user_recognized = True
                #GPIO.output(21, 1)                  #Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
                #time.sleep(2)                     #Hold the GPIO pin High for 2 Minutes
                break

            else:
                print("Invalid Pin, try again.")
                lcd.lcd_clear()
                lcd.lcd_display_string("Invalid Pin,", 1)
                lcd.lcd_display_string("Try again", 2)



#If GPIO from MSP430 to the Pi for the Sonar Sensor is set, there is someone within 2m of the door so run the SpeechRecognition function
### NEED TO SET UP WITH GPIO Pins WE WANT TO USE ###
#if(GPIO.input(20)):
#    speech()

speech()


