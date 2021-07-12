import speech_recognition as sr

r = sr.Recognizer()

message = 'empty'

while True:
    with sr.Microphone() as source:
        print('Speak: ')
        
        audio = r.listen(source)
        
        try:
            text = r.recognize_google(audio)
            #print('You said : {}'.format(text))
            print('You said : ' + text)
            message = text
            if message == 'exit':
                break
        except sr.UnknownValueError:
            print('Google Speech did not recognize audio')
        except sr.RequestError as e:
            print('Could not request results from Google Speech Recognition Service; {0}'.format(e))
            
print(message)