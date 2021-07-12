import speech_recognition as sr
import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)

#Set GPIO Pin 21 as Output, and set an internal Pull-Down Resistor 
#GPIO.setup(21, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

def speech():
    r = sr.Recognizer()

    message = 'empty'
    time_left = 120

    while (time_left != 0):
        with sr.Microphone() as source:
            print('Speak: ')
            
            audio = r.listen(source)
            
            try:
                text = r.recognize_google(audio)
                #print('You said : {}'.format(text))
                print('You said : ' + text)
                message = text
                if message == '4321':
                    print("Pin Number Detected...")
                    GPIO.output(21, 1)                  #Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
                    time.sleep(120)                     #Hold the GPIO pin High for 2 Minutes
                if message == 'exit':
                    break
            except sr.UnknownValueError:
                print('Google Speech did not recognize audio')
            except sr.RequestError as e:
                print('Could not request results from Google Speech Recognition Service; {0}'.format(e))
        time.sleep(1)
        time_left = time_left - 1

#If GPIO from MSP430 to the Pi for the Sonar Sensor is set, there is someone within 2m of the door so run the SpeechRecognition function
### NEED TO SET UP WITH GPIO Pins WE WANT TO USE ###
#if(GPIO.input(1)):
#    speech()

speech()
