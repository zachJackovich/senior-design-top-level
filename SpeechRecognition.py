import I2C_LCD_driver
import speech_recognition as sr
import RPi.GPIO as GPIO
import time
from keypad_v2 import keypad

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

#Set GPIO 12 as Input (MSP430 -> Pi), and set an internal Pull-Down Resistor 
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Set GPIO 16 as Output (Pin # Pi -> Facerep Pi for LED Status Lights), but initialize the output to 0
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

#Set GPIO 6 as Output (Pi -> MSP430), no Pull-down resistor needed on outputs, but initialize the output to 0
GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW) 

# Users pin definitions
Adam = '1234'
Moisess = '4321'
Reham = '5678'
Zach = '8765'

#Global variable to track unauthorized attempts
#unauthorized_attempts = 0

def speech():
    r = sr.Recognizer()
    message = 'empty'
    
    recognition_tries = 5

    while (recognition_tries != 0):

        with sr.Microphone() as source:
            
            print('Speech or Keypad?')   
            lcd.lcd_clear()
            lcd.lcd_display_string("Speech or", 1)
            lcd.lcd_display_string("Keypad?", 2)
            audio = r.listen(source)
            
            try:
                text = r.recognize_google(audio)

                print('You said : ' + text)
                message = text
                
                if message == 'speech':
                    listen_for_pin()

                elif message == 'keypad':
                    keypad_function()

                else:
                    print ("invalid input!!")
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Invalid Input,", 1)
                    lcd.lcd_display_string("Try again", 2)
                    time.sleep(5)
                
            except sr.UnknownValueError:
                print('Did not recognize audio')
            except sr.RequestError as e:
                print('Could not recognize speech during analysis; {0}'.format(e))

        recognition_tries = recognition_tries - 1

    return


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
                GPIO.output(6, 1)                  # Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
                GPIO.output(16, 1)                       # Set the GPIO to the Facereq Pi, signaling that Pin is authenticated
                time.sleep(10)                     # Hold the GPIO pin High for 2 Minutes

                # After waiting X minutes, clear LCD and reset GPIO outputs Low
                lcd.lcd_clear()
                GPIO.output(6, 0)
                GPIO.output(16, 0)
                user_recognized = True
                break

            elif message == '4321':
                # Display welcome message to Moisess
                print("Pin Number Detected...")
                lcd.lcd_clear()
                lcd.lcd_display_string("Welcome Home,", 1)
                lcd.lcd_display_string("Moisess!", 2)
                GPIO.output(6, 1)                  # Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
                GPIO.output(16, 1)                       # Set the GPIO to the Facereq Pi, signaling that Pin is authenticated
                time.sleep(10)                     # Hold the GPIO pin High for 2 Minutes

                # After waiting X minutes, clear LCD and reset GPIO outputs Low
                lcd.lcd_clear()
                GPIO.output(6, 0)
                GPIO.output(16, 0)
                user_recognized = True
                break

            elif message == '5678':
                # Display welcome message to Reham
                print("Pin Number Detected...")
                lcd.lcd_clear()
                lcd.lcd_display_string("Welcome Home,", 1)
                lcd.lcd_display_string("Reham!", 2)
                GPIO.output(6, 1)                  # Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
                GPIO.output(16, 1)                       # Set the GPIO to the Facereq Pi, signaling that Pin is authenticated
                time.sleep(10)                       # Hold the GPIO pin High for 2 Minutes

                # After waiting X minutes, clear LCD and reset GPIO outputs Low
                lcd.lcd_clear()
                GPIO.output(6, 0)
                GPIO.output(16, 0)
                user_recognized = True
                break

            elif message == '8765':
                # Display welcome message to Zach
                print("Pin Number Detected...")
                lcd.lcd_clear()
                lcd.lcd_display_string("Welcome Home,", 1)
                lcd.lcd_display_string("Zach!", 2)
                GPIO.output(6, 1)                  # Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
                GPIO.output(16, 1)                       # Set the GPIO to the Facereq Pi, signaling that Pin is authenticated
                time.sleep(10)                     # Hold the GPIO pin High for 2 Minutes

                # After waiting X minutes, clear LCD and reset GPIO outputs Low
                lcd.lcd_clear()
                GPIO.output(6, 0)
                GPIO.output(16, 0)
                user_recognized = True
                break

            else:
                print("Invalid Pin, try again.")
                lcd.lcd_clear()
                lcd.lcd_display_string("Invalid Pin,", 1)
                lcd.lcd_display_string("Try again", 2)
                time.sleep(5)


def keypad_function():
    kp = keypad(columnCount = 4)
    user_recognized = False

    lcd.lcd_clear()
    lcd.lcd_display_string("Enter your Pin", 1)
    print("Enter Pin Number")

    while not user_recognized:
        ###### 4 Digit wait ######
        seq = ''
        for i in range(4):
            digit = None
            while digit == None:
                digit = kp.getKey()
                char_version = str(digit)
            seq = seq + char_version
            time.sleep(0.4)

        if seq == '1234':
            # Display welcome message to Adam
            print("Pin Number Detected...")
            lcd.lcd_clear()
            lcd.lcd_display_string("Welcome Home,", 1)
            lcd.lcd_display_string("Adam!", 2)
            GPIO.output(6, 1)                  # Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
            GPIO.output(16, 1)                       # Set the GPIO to the Facereq Pi, signaling that Pin is authenticated
            time.sleep(10)                     # Hold the GPIO pin High for 2 Minutes

            # After waiting X minutes, clear LCD and reset GPIO outputs Low
            lcd.lcd_clear()
            GPIO.output(6, 0)
            GPIO.output(16, 0)
            user_recognized = True
            break

        elif seq == '4321':
            # Display welcome message to Moisess
            print("Pin Number Detected...")
            lcd.lcd_clear()
            lcd.lcd_display_string("Welcome Home,", 1)
            lcd.lcd_display_string("Moisess!", 2)
            GPIO.output(6, 1)                  # Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
            GPIO.output(16, 1)                       # Set the GPIO to the Facereq Pi, signaling that Pin is authenticated
            time.sleep(10)                     # Hold the GPIO pin High for 2 Minutes

            # After waiting X minutes, clear LCD and reset GPIO outputs Low
            lcd.lcd_clear()
            GPIO.output(6, 0)
            GPIO.output(16, 0)
            user_recognized = True
            break

        elif seq == '5678':
            # Display welcome message to Reham
            print("Pin Number Detected...")
            lcd.lcd_clear()
            lcd.lcd_display_string("Welcome Home,", 1)
            lcd.lcd_display_string("Reham!", 2)
            GPIO.output(6, 1)                  # Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
            GPIO.output(16, 1)                       # Set the GPIO to the Facereq Pi, signaling that Pin is authenticated
            time.sleep(10)                       # Hold the GPIO pin High for 2 Minutes
            
            # After waiting X minutes, clear LCD and reset GPIO outputs Low
            lcd.lcd_clear()
            GPIO.output(6, 0)
            GPIO.output(16, 0)
            user_recognized = True
            break

        elif seq == '8765':
            # Display welcome message to Zach
            print("Pin Number Detected...")
            lcd.lcd_clear()
            lcd.lcd_display_string("Welcome Home,", 1)
            lcd.lcd_display_string("Zach!", 2)
            GPIO.output(6, 1)                  # Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
            GPIO.output(16, 1)                 # Set the GPIO to the Facereq Pi, signaling that Pin is authenticated
            time.sleep(10)                     # Hold the GPIO pin High for 2 Minutes

            # After waiting X minutes, clear LCD and reset GPIO outputs Low
            lcd.lcd_clear()
            GPIO.output(6, 0)
            GPIO.output(16, 0)
            user_recognized = True
            break

        else:
            print("Invalid Pin, try again.")
            lcd.lcd_clear()
            lcd.lcd_display_string("Invalid Pin,", 1)
            lcd.lcd_display_string("Try again", 2)
            time.sleep(5)


def main():
    #If GPIO from MSP430 to the Pi for the Sonar Sensor is set, there is someone within 2m of the door so run the SpeechRecognition function
    
    print("Welcome...")
    master_pin = input("Please enter a Master Pin Number...")

    print("Thank you. Now starting the Smart Door Security System...")
    
    while True:
        if(GPIO.input(12)):
            print("GPIO from MSP430 set HIGH. Running Speech()...")
            time.sleep(3)
            speech()
        


if __name__ == "__main__":
    main()