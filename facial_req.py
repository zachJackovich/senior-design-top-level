#! /usr/bin/python

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import subprocess
import RPi.GPIO as GPIO
import datetime

subprocess.call(['sh', './redLED.sh']) #Turn the LED red to indicate the pi is on

# Setup GPIO Use
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO from Pi to MSP430
GPIO.setup(6, GPIO.OUT)
#GPIO from Pi to Pi
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO from MSP430 to Pi
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# loop over frames from the video file stream

time.sleep(1)


def facialRec():
    subprocess.call(['sh', './whiteLED.sh']) #Turn the LED white
    #Initialize 'currentname' to trigger only when a new person is identified.
    currentname = "unknown"
    #Determine faces from encodings.pickle file model created from train_model.py
    encodingsP = "encodings.pickle"
    #use this xml file
    cascade = "haarcascade_frontalface_default.xml"

    # load the known faces and embeddings along with OpenCV's Haar
    # cascade for face detection
    #print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())
    detector = cv2.CascadeClassifier(cascade)

    # initialize the video stream and allow the camera sensor to warm up
    #print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

    # start the FPS counter
    fps = FPS().start()
    valid = False
    user_recognized = False
    # setting the max time for this function to run to 2 mins
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
    
    while not(user_recognized):
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        
        # convert the input frame from (1) BGR to grayscale (for face
        # detection) and (2) from BGR to RGB (for face recognition)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect faces in the grayscale frame
        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
            minNeighbors=5, minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

        # OpenCV returns bounding box coordinates in (x, y, w, h) order
        # but we need them in (top, right, bottom, left) order, so we
        # need to do a bit of reordering
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []



        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                encoding)
            name = "Unknown" #if face is not recognized, then print Unknown

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)
                
                #If someone in your dataset is identified, print their name on the screen
                if currentname != name:
                    currentname = name
                    user_recognized = True
                    print("The user is: " + currentname)
                    
                    if ((currentname == 'Moisess') or (currentname == 'Zach')):
                        #set the valid bit to true
                        valid = True
 			new_end_time = datetime.datetime.now() + datetime.timedelta(seconds=30)
			GPIO.output(6, 1) # Set the GPIO to the MSP430 to High, signaling the U$
			while True:
                                if(GPIO.input(12)):
                                       print("Speech and face recognized, changing LEDs to green")
                                       subprocess.call(['sh', './greenLED.sh']) #Turn the LED Green
                                       break
                                if datetime.datetime.now() >= new_end_time:
                                       print ('inner time limit reached')
                                       break
			time.sleep(60)
			GPIO.output(6, 0)

#                        if(GPIO.input(12) and valid == True):
#                            print("Speech and face recognized, changing LEDs to green")
#                            subprocess.call(['sh', './greenLED.sh']) #Turn the LED Green
#                            GPIO.output(6, 1) # Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
#                            time.sleep(240)
#                            GPIO.output(6, 0)
#                        elif(GPIO.input(12) or valid == True):
#                            print("Speech Recognized or Face Recognized, changing LEDs to blue")
#                            subprocess.call(['sh', './greenLED.sh']) #Turn the LED Yellow
#                            time.sleep(3)
#			    GPIO.output(6, 1) # Set the GPIO to the MSP430 to High, signaling the User's Pin# was detected
#			    new_end_time = datetime.datetime.now() + datetime.timedelta(seconds=30)
#			    while True:
#                                if(GPIO.input(12) and valid == True):
#					print("Speech and face recognized, changing LEDs to green")
#                                 	subprocess.call(['sh', './greenLED.sh']) #Turn the LED Green
#					break
#                                if datetime.datetime.now() >= new_end_time:
#                                	print ('time limit reached')
#                                 	break

#			    time.sleep(60)
#                            GPIO.output(6, 0)
                            
                       # elif(GPIO.input(12) or valid == True):
                           # print("Face Recognized but not speech, changing LEDs to blue")
                            #subprocess.call(['sh', './blueLED.sh']) #Turn the LED Blue
                            
                            # setting the max time for this function to run to 2 mins
                            #new_end_time = datetime.datetime.now() + datetime.timedelta(seconds=30)
                            
                            #GPIO.output(6, 1) # Set the GPIO to the MSP430 to High, signaling the User's Pin# 
                            #while True:
                               # if(GPIO.input(12) and valid == True):
                                #    print("Speech and face recognized, changing LEDs to green")
                                 #   subprocess.call(['sh', './greenLED.sh']) #Turn the LED Green
                                #if valid or datetime.datetime.now() >= newend_time:
                                 #   print ('time limit reached')
                                  #  break
                           #time.sleep(5)
                            #GPIO.output(6, 0)
                            #break
                    else:
                        print ('Unauthorized user!')
                        subprocess.call(['sh', './redLED.sh']) #Turn the LED red
                        time.sleep(2)
                        
                        
                time.sleep(1)
                
            # update the list of names
            names.append(name)

        # update the FPS counter
        fps.update()
        #if the user is identified or the time limit is reached then exit
        if valid or datetime.datetime.now() >= end_time:
            print ('time limit reached')
            break
    # stop the timer and display FPS information
    fps.stop()
    print("Ending facialRec()...")
    subprocess.call(['sh', './offLED.sh']) #Turn the LED off
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
    time.sleep(10)
    #If GPIO from MSP430 to the Pi for the Sonar Sensor is set, there is someone within 2m of the door so run the SpeechRecognition functio


def main():
    #If GPIO from MSP430 to the Pi for the Sonar Sensor is set, there is someone within 2m of the door so run the SpeechRecognition function

    print("Thank you. Now starting the Smart Door Security System...")
    subprocess.call(['sh', './offLED.sh']) #Turn the LED off
    while True:
        try:
            if(GPIO.input(16)):
#		subprocess.call(['sh', './offLED.sh']) #Turn the LED off
            	print("GPIO from MSP430 set HIGH. Running facialRec()...")
            	time.sleep(3)
            	facialRec()
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            #subprocess.call(['sh', './runLEDs.sh']) #Turn the LEDs different colors
            subprocess.call(['sh', './offLED.sh']) #Turn the LED off
            GPIO.output(6, 0)
	    #GPIO.cleanup()
            break
            

if __name__ == "__main__":
    main()
