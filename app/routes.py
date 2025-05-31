from flask import request, Flask
from flask_restful import Resource, Api
from app.controller import MessageController
from app.models import MessageSchema
from pydantic import ValidationError

class MessageResource(Resource):
    """
    Recurso da API para manipulação de mensagens.
    """

    def __init__(self):
        self.controller = MessageController()
        self.message_schema = MessageSchema()

    def post(self):
        """
        Cria uma nova mensagem.
        """
        try:
            MessageSchema(**request.json)
            data = request.json
        except ValidationError as e:
            return {"success": False, "message": "Validation errors", "errors": e.errors()}, 400
        except Exception as e:
            return {"success": False, "message": "Invalid JSON payload", "errors": str(e)}, 400

        return self.controller.create_message(data)

    def get(self, message_id=None):
        """
        Retorna mensagem(s) pelo ID ou lista todas.
        """
        if message_id:
            return self.controller.get_message(message_id)
        return self.controller.list_messages()

class HealthCheck(Resource):
    """
    Endpoint de verificação de saúde do serviço.
    """
    def get(self):
        return {"status": "active", "version": "1.0.0", "message": "HelpBot service is healthy."}

def register_routes(app: Flask):
    """
    Registra as rotas da API na aplicação Flask.
    """
    api = Api(app)
    api.add_resource(MessageResource,
                     '/api/v1/messages',
                     '/api/v1/messages/<string:message_id>')
    api.add_resource(HealthCheck, '/health')
