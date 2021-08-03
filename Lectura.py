import speech_recognition as sr                     #importa los paquetes de audios grbados y demas



def Entrada (E_Audio):
    r = sr.Recognizer()
    with sr.Microphone() as E_Audio:
        audio = r.listen(E_Audio)
    try:
        text = r.recognize_google(audio)
        return print("Palabra: {}".format(text))
    except:
        return print("No se reconoció la palabra")