import os
import tempfile

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import azure.cognitiveservices.speech as speechsdk

from main import MICROSOFT_API_KEY

speech_bp = Blueprint('speech', __name__)
api = Api(speech_bp)


class TextToSpeech(Resource):
    def post(self):
        data = request.get_json()
        language = data.get("language")
        text = data.get("text")

        if not language or not text:
            return {"error": "Se requiere 'language' y 'text'"}, 400

        # Aquí iría la lógica de Text-to-Speech
        # response = generar_audio(text, language)

        return {"message": "Texto recibido para TTS", "language": language, "text": text}, 200



class PronunciationAssessment(Resource):
    def post(self):
        language = request.form.get("language")
        file = request.files.get("file")
        reference_text = request.form.get("text")  # opcional

        if not language or not file:
            return {"error": "Se requiere 'language' y un archivo"}, 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            temp_path = tmp.name
            file.save(temp_path)

        try:
            # Configuración de Azure Speech
            speech_key = MICROSOFT_API_KEY
            region = "eastus2"
            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
            audio_config = speechsdk.audio.AudioConfig(filename=temp_path)

            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                language=language,
                audio_config=audio_config
            )

            pronunciation_config = speechsdk.PronunciationAssessmentConfig(
                reference_text=reference_text or "",
                grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
                granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
                enable_miscue=True
            )
            pronunciation_config.n_best_phoneme_count = 5
            pronunciation_config.apply_to(speech_recognizer)

            # Evaluación
            result = speech_recognizer.recognize_once()
            pron_result = speechsdk.PronunciationAssessmentResult(result)

            # Generar feedback por palabra
            feedback = []
            for word in pron_result.words:
                word_info = {
                    "word": word.word,
                    "accuracy_score": word.accuracy_score,
                    "error_type": word.error_type,
                    "phonemes": []
                }
                for phoneme in word.phonemes:
                    phoneme_info = {
                        "phoneme": phoneme.phoneme,
                        "accuracy_score": phoneme.accuracy_score,
                        "nbest": []
                    }
                    if phoneme.nbest_phonemes is not None:
                        for n in phoneme.nbest_phonemes:
                            phoneme_info["nbest"].append({"phoneme": n.phoneme, "score": n.score})
                    word_info["phonemes"].append(phoneme_info)
                feedback.append(word_info)

            return jsonify({
                "message": "Evaluación completada",
                "language": language,
                "filename": file.filename,
                "feedback": feedback,
                "overall_scores": {
                    "accuracy": pron_result.accuracy_score,
                    "fluency": pron_result.fluency_score,
                    "completeness": pron_result.completeness_score,
                    "pronunciation": pron_result.pronunciation_score
                }
            })

        finally:
            # Eliminar archivo temporal
            if os.path.exists(temp_path):
                os.remove(temp_path)

class BatchTranscription(Resource):
    def post(self):
        language = request.form.get("language")
        file = request.files.get("file")

        if not language or not file:
            return {"error": "Se requiere 'language' y un archivo"}, 400

        # Aquí iría la lógica de Batch Transcription
        # transcripcion = transcribir_archivo(file, language)

        return {"message": "Archivo recibido para transcripción", "language": language, "filename": file.filename}, 200



api.add_resource(TextToSpeech, "/text-to-speech")
api.add_resource(PronunciationAssessment, "/speech-to-text/pronunciation-assessment")
api.add_resource(BatchTranscription, "/speech-to-text/batch-transcription")
