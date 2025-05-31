import logging
from datetime import datetime
from bson import ObjectId
from app import mongo
from app.services.openai_service import OpenAIService
from app.services.n8n_integration import N8nIntegration
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)

class MessageController:
    """
    Controlador para operações relacionadas a mensagens.
    """

    def __init__(self):
        self.openai = OpenAIService()
        self.n8n = N8nIntegration()

    def create_message(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        Cria uma nova mensagem, opcionalmente processa com IA e envia ao n8n.
        """
        try:
            message_payload = {
                "content": data['content'],
                "user_id": data.get('user_id'),
                "timestamp": datetime.utcnow(),
                "status": "received",
                "ai_response": None
            }

            if self.openai.is_enabled():
                ai_generated_response = self.openai.generate_response(data['content'])
                if ai_generated_response:
                    message_payload['ai_response'] = ai_generated_response
                    message_payload['status'] = 'processed_by_ai'
                else:
                    message_payload['status'] = 'ai_processing_failed'
            else:
                message_payload['status'] = 'ai_disabled'

            result = mongo.db.messages.insert_one(message_payload.copy())
            created_message = message_payload.copy()
            created_message['_id'] = str(result.inserted_id)

            # Envia para n8n (se habilitado)
            if self.n8n.is_enabled():
                webhook_success = self.n8n.send_to_webhook(created_message)
                if not webhook_success:
                    logger.warning(f"Failed to send message {created_message['_id']} to n8n webhook.")

            # Serializa timestamp
            created_message_response = created_message.copy()
            created_message_response['timestamp'] = created_message_response['timestamp'].isoformat()

            return {"success": True, "message": "Message created successfully.", "data": created_message_response}, 201

        except Exception as e:
            logger.error(f"Error creating message: {str(e)}")
            return {"success": False, "message": "An unexpected error occurred.", "errors": str(e)}, 500

    def get_message(self, message_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Busca uma mensagem específica pelo seu ID.
        """
        try:
            if not ObjectId.is_valid(message_id):
                return {"success": False, "message": "Invalid message ID format."}, 400

            message = mongo.db.messages.find_one({"_id": ObjectId(message_id)})
            if message:
                message['_id'] = str(message['_id'])
                if isinstance(message.get('timestamp'), datetime):
                    message['timestamp'] = message['timestamp'].isoformat()
                return {"success": True, "data": message}, 200

            return {"success": False, "message": "Message not found."}, 404

        except Exception as e:
            logger.error(f"Error getting message: {str(e)}")
            return {"success": False, "message": "An unexpected error occurred while retrieving the message.", "errors": str(e)}, 500

    def list_messages(self) -> Tuple[Dict[str, Any], int]:
        """
        Lista as últimas 100 mensagens armazenadas.
        """
        try:
            messages_cursor = mongo.db.messages.find().sort("timestamp", -1).limit(100)
            messages_list = []
            for msg in messages_cursor:
                msg['_id'] = str(msg['_id'])
                if isinstance(msg.get('timestamp'), datetime):
                    msg['timestamp'] = msg['timestamp'].isoformat()
                messages_list.append(msg)
            return {"success": True, "count": len(messages_list), "data": messages_list}, 200
        except Exception as e:
            logger.error(f"Error listing messages: {str(e)}")
            return {"success": False, "message": "An unexpected error occurred while listing messages.", "errors": str(e)}, 500
