from builtins import print, type, enumerate
from datetime import datetime
from telegram.ext import *
import speech_recognition
import speech_recognition as sr




def ejemplo_respuesta(entrata_texto):

    user_message = str(entrata_texto).lower()

    if user_message in ("hola", "hi"):
        return "Hey!\n¿Como estas ✨? :D"

    if user_message in ("bien", "Biem", "mas o menos"):
        return "Bueno :>"

    if user_message in ("mal", "Mal"):
        return "Bueno, que tengas un mejor día "

    if user_message in ("Gracias", "gracias"):
        return "De nada ✨"

    if user_message in ( "Quien eres ?", "how are you?", "quien eres ?", "Quién eres ?"):
        return "Yo sou un Bot de telegram "

    if user_message in ( "que haces ?", "que haces?", "que haces"):
        return "leyendo tus mensajes xdddd "

    if user_message in ("Como estas ?", "como estas ?"):
        return "Activo 24/7 mijo :> "

    if user_message in ("tiempo", "que hora es ?", "que dia es hoy?","time"):
        now = datetime.now()
        date_time = now.strftime("Fecha: %d/%m/%y  Hora: %H:%M:%S")
        return str(date_time)


    return "No te entiendo bro :c"
