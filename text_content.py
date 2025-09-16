from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

text_bp = Blueprint("text", __name__, url_prefix="/text-services")
api = Api(text_bp)


class GenerateContent(Resource):
    def post(self):
        """
        Endpoint para generar contenido a partir de un texto.
        JSON esperado:
        {
            "language": "es",
            "text": "Escribe un artículo sobre IA"
        }
        """
        data = request.get_json()
        language = data.get("language")
        text = data.get("text")

        if not language or not text:
            return {"error": "Se requiere 'language' y 'text'"}, 400

        # Lógica de generación de contenido
        # content = generar_contenido(text, language)

        return {"message": "Contenido generado", "language": language, "text": text}, 200


class GenerateChatContent(Resource):
    def post(self):
        """
        Endpoint para generar contenido tipo chat.
        JSON esperado:
        {
            "language": "es",
            "messages": [
                {"role": "user", "content": "Hola, ¿cómo estás?"},
                {"role": "assistant", "content": "¡Hola! Estoy bien, gracias."}
            ]
        }
        """
        data = request.get_json()
        language = data.get("language")
        messages = data.get("messages")

        if not language or not messages:
            return {"error": "Se requiere 'language' y 'messages'"}, 400

        # Lógica de generación tipo chat
        # chat_response = generar_chat(messages, language)

        return {"message": "Respuesta generada de chat", "language": language, "messages": messages}, 200


# Registramos recursos en este blueprint
api.add_resource(GenerateContent, "/generate-content")
api.add_resource(GenerateChatContent, "/generate-chat-content")
