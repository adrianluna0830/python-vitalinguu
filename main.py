from flask import Flask
from flask_restful import Api, Resource
from google import genai
import azure.cognitiveservices.speech as speechsdk

import os


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MICROSOFT_API_KEY = os.getenv("MICROSOFT_API_KEY")


client = genai.Client(api_key=GEMINI_API_KEY)
chat = client.chats.create(model="gemini-2.5-flash-lite")
app = Flask(__name__)
api = Api(app)

# from api.users import users_bp
# from api.products import products_bp
#
# app = Flask(__name__)
#
# # Registramos ambos blueprints en la app principal
# app.register_blueprint(users_bp)
# app.register_blueprint(products_bp)
# app.run(debug=True,port=5000)
if __name__ == "__main__":
    # Configurar las credenciales (reemplaza con tus valores)
    speech_key = MICROSOFT_API_KEY  # Clave de tu recurso de Speech Services
    service_region = "eastus2"  # Región donde creaste el recurso (ej: "eastus")

    # Configurar el servicio de speech
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Configurar la voz (opcional - por defecto usa voz en inglés)
    speech_config.speech_synthesis_voice_name = "de-DE-KatjaNeural"  # Voz en español mexicano

    # Crear el sintetizador
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Texto a convertir
    text = "Deutsch ist eine wunderschöne Sprache, die von Millionen Menschen auf der ganzen Welt gesprochen wird. Am Anfang kann es schwierig erscheinen, die Grammatik und die langen Wörter zu verstehen. Mit Geduld und regelmäßiger Übung wird es jedoch einfacher."

    # Convertir texto a voz
    result = synthesizer.speak_text_async(text).get()

    # Verificar el resultado
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Síntesis completada exitosamente!")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Síntesis cancelada: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error: {cancellation_details.error_details}")