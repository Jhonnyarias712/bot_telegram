import speech_recognition as sr
import pyaudio
sr.__version__

r = sr.Recognizer()
#archivo= sr.AudioFile('F-01.wav')

with sr.Microphone() as source:
    audio=r.listen(source)
    text= r.recognize_google(audio)
    print(text)
