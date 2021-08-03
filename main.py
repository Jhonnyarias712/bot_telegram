from builtins import print
from turtle import update
import speech_recognition as sr
import requests
import json
import io
import os
import random
#from google.cloud import speech
#from google.cloud import storage
import telegram
from pymediainfo import MediaInfo
from Tools.scripts.var_access_benchmark import A
import subprocess
import Constants as keys
from telegram.ext import *
from telegram import ChatAction, Update, Message, Voice
import Responses as R
import Lectura as L
import speech_recognition as sr
#speech_client = speech.SpeechClient()
#storage_client = storage.Client("E:\Json de google speech")
BUCKET_NAME = os.getenv('VOICOS_BUCKET')
print("Iniciando.... Bot")

def star_command(update,context):                    #definimos la funcion del manejador el cual el despachador necesita
    update.message.reply_text(f"Holaaaaaa ✨")
    update.message.reply_text(f"🤩Biemvenido ! { update.message.from_user.full_name} ✨ mi nombre es Emot\nsoy un bot de telegram y mi funcion es\npredecir tu estado de animo con un audio de voz\nque tu me envies para mas informacion /info")


def help_command(update, context):
    update.message.reply_text("Si Necesitas ayuda busca a dios ♥, \nConsulta a google bro 😉")

def handle_message(update, context):
    text = str(update.message.text).lower()
    responses = R.ejemplo_respuesta(text)
    update.message.reply_text(responses)  # = R.ejemplo_respuesta(responses)

def transcribe(file_name: str, to_gs: bool, lang_code: str = 'es-EC'):
    media_info = MediaInfo.parse(file_name)
    r= sr.Recognizer()
    if len(media_info.audio_tracks) != 1 or not hasattr(media_info.audio_tracks[0], 'sampling_rate'):
        try:
            texto = r.recognize_google(file_name,lang_code,to_gs )
            update.message.reply_text(f"Dijiste: {texto}")
        except:
            update.message.reply_text("Esto es un audio de voz pero no lo entendi por su formato solo se admite WAV")

def download_and_prep(file_name: str, message: Message, voice: Voice) -> bool:
    voice.get_file().download(file_name)
    message.reply_chat_action(action=ChatAction.TYPING)
    return voice.duration > 58

def voice_to_text(update: Update, context: CallbackContext) -> None:
    r = sr.Recognizer()
    archivo = sr.AudioFile("F-01.wav")
    chat_id = update.effective_message.chat.id
    file_name = '%s_%s%s.ogg' % (chat_id, update.message.from_user.id, update.message.message_id)
    to_gs = download_and_prep(file_name, update.effective_message, update.effective_message.voice)
    update.message.reply_text("Esto es un mensaje de voz.. estamos trabajando para poder adquirir datos")
    numero = random.randint(0, 4)
    tiempo_duracion= str(update.message.voice.duration)
    update.message.reply_text(f"Su audio tiene {tiempo_duracion} segundos de duracion :>")
    if numero == 1:
        update.message.reply_text("Estado de ánimo: Negativo 😭")
    if numero == 0:
        update.message.reply_text("Estado de ánimo: Positvo  ☺")
    if numero == 2:
        update.message.reply_text("Estado de ánimo: Neutro  😐")
    if numero == 3:
        update.message.reply_text("Estado de ánimo: Triste ☹")
    if numero == 4:
        update.message.reply_text("Estado de animo: Feliz 😃")
    update.message.reply_voice(update.message.voice.get_file().file_id)
    #text= r.recognize_google(update.message.voice.get_file().file_id)
    try:
        with archivo as source:
            update.message.reply_text("su audio esta siendo procesado")
            audioA= r.record(source)
            r.recognize_google(audioA)
            print(r.recognize_google(audioA))
            update.message.reply_text(audioA, languaje="es-EC")
        #audio= r.record(update.message.voice.get_file())
        #texto = r.recognize_google(r.listen(audio), language="es-EC")
        #update.message.reply_text(f"Dijiste: {texto}")
    except:
        update.message.reply_text(f"OK {update.message.from_user.full_name}")

def handle_audio(update, context):
    audio = context.bot.get_file(file_id=update.message.audio.file_id)     #Solo par archivos de audio ejemplo: mp3
    audio.download()
    update.message.reply_text("Su audio esta siendo procesado....")
    r= sr.Recognizer()
    try:
        audio= r.listen(audio)
        texto = r.recognize_google(audio.get_file(),language="es-EC")
        update.message.reply_text(f"Dijiste: {texto}")
    except:
        update.message.reply_text("Estoi es un audio de voz pero no lo entendi ")
def get_audio_messages(update,message):
    r = sr.Recognizer()
    file_info = update.get_file(message.voice.file_id)
    downloaded_file = update.download_file(file_info.file_path)
    with open('user_voice.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)

    src_filename = 'user_voice.ogg'
    dest_filename = 'user_voice_output.flac'

    process = subprocess.run(['C:\\ffmpeg\\bin\\ffmpeg.exe', '-i', src_filename, dest_filename])
    if process.returncode != 0:
        raise Exception("Something went wrong")

    with open('user_voice_output.flac', 'rb') as user_audio:
        text = r.recognize_google(user_audio)
        update.message.reply_text(message.from_user.id, text)

def handle_voice_Message(self,update,context):
    r=sr.Recognizer(update.voice.get_file(file_id=update.voice.file_id))
    Audio_voz= self._get_file()

    try:
        text = r.recognize_google(Audio_voz)
        print('You said: {}'.format(text))
        update.voice.reply_text(f"Tu dijiste: {text}")

    except:
        print('Sorry could not hear')
    update.message.reply_text("Estoi es un audio de voz ")

#*****************************************
def get_voice_transcript(self, file_content):
    IBM_API_URL = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/41ca9fb2-3937-4268-ad74-607eda41bf40'
    response = requests.post(url=IBM_API_URL,
                             data=file_content,
                             headers={'Content-Type': self.value['mime_type']},
                             auth=('apikey', 'Cww1jJ0JImdXXuJDDNV1eg6wA1SsQsNNO7Nl0zNHRj3n'))
    json_response = json.loads(response.content)
    if response.status_code != 200 or not json_response.get('results'):
        return 'Could not hear you well!'
    return json_response['results'][0]['alternatives'][0]['transcript']

def voice_get_response(self):
    try:
        file_content = self._get_file()
        voice_transcript = self._get_voice_transcript(file_content)
        response = {
            'text': voice_transcript,
        }
    except FileNotFoundError:
        response = {
            'text': 'Could not get your voice message!'
        }
    method_name = 'sendMessage'
    update.message.reply_text(method_name,response)
    #return method_name, response
#*****************************************
def menu_command (update,context):
    update.message.reply_text("Hola♥ \naqui algunas funciones que puede hacer en este bot:\n/Start, /help, /menu, /info \n")

def info_command(update,context):
    update.message.reply_text(f"{update.message.from_user.full_name} este es un bot de telegram {update.message.bot.first_name} y su unico objetivo es predecir tu estado de animo e informarte la hora escribe \"time,tiempo\"")

def error(update, context):
    print(f"update{update} caused error {context.error}")

def main ():
    updater = Updater(keys.API_KEY, use_context=True)           #llamamos al bot de telegran de manera local es decir mientras la ejecucion dure
    dp = updater.dispatcher                                     #despachador del bot
    dp.add_handler(CommandHandler("start", star_command))       #el despachador se encarga de manejar los comandos es decir las entradas con barra "/"
    dp.add_handler(CommandHandler("help", help_command))        #otro ejemplo de comando
    dp.add_handler(CommandHandler("menu", menu_command))
    dp.add_handler(CommandHandler("info", info_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))    #El despachador maneja las entradas de texto y recive un tipo de texto el cual filta en el mensaje y ejecuta la funcion y esa funcion se encarga de procesar lo que uno haya programado
    dp.add_handler(MessageHandler(Filters.audio, handle_audio))                                                 # ente es el despachador que no pme sale :c *************** help *******************
    dp.add_handler(MessageHandler(Filters.voice, voice_to_text))
    dp.add_error_handler(error)                                     # despachador de posibles errores en la ejecucion

    updater.start_polling(1)                                        #tiempo de respuesta del bot expresada en segundo
    updater.idle()                                                  #permite la terminacion de bot con "Control+c"

main()                         #funcion/metodo principal main