#pip install pyaudio
#pip install SpeechRecognition

import speech_recognition as sr
r = sr.Recognizer()

with sr.Microphone() as source:
    print('Say Something!')
    audio = r.listen(source)

try:
    result = r.recognize_google(audio,language="sv-SE")
    print("Google thinks you said:\n" + result)
    if result == "hej":
        print("Yay")
except Exception as e:
    print(e)