import logging
from openai import OpenAI
from config import Config  # Importar Config do root
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class OpenAIService:
    """
    Serviço para integração com a API da OpenAI.
    Responsável por gerar respostas de IA via chat completions.
    """

    def __init__(self):
        self.api_key: Optional[str] = Config.OPENAI_API_KEY
        self.enabled: bool = bool(self.api_key)
        if self.enabled:
            self.client = OpenAI(api_key=self.api_key)
            self.model = Config.OPENAI_MODEL
            self.temperature = Config.OPENAI_TEMPERATURE
            self.max_tokens = Config.OPENAI_MAX_TOKENS
        else:
            self.client = None
            logger.warning("OPENAI_API_KEY not configured. OpenAI service disabled.")

    def is_enabled(self) -> bool:
        """
        Retorna True se a integração com a OpenAI está habilitada.
        """
        return self.enabled

    def generate_response(self, prompt: str) -> Optional[str]:
        """
        Gera uma resposta de IA a partir de um prompt de usuário.
        """
        if not self.is_enabled() or not self.client:
            logger.warning("OpenAI service is disabled. Cannot generate response.")
            return None
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um assistente virtual de uma pequena empresa. Responda de forma clara e concisa."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            logger.info("OpenAI response generated successfully.")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return None
