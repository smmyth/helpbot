import logging
import requests
from config import Config  # Importar Config do root
from typing import Any, Dict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class N8nIntegration:
    """
    Serviço para integração com webhooks do n8n.
    Responsável por enviar dados a fluxos automatizados.
    """

    def __init__(self):
        self.webhook_url: str = Config.N8N_WEBHOOK_URL
        self.enabled: bool = bool(self.webhook_url)

    def is_enabled(self) -> bool:
        """
        Retorna True se a integração com o n8n está habilitada.
        """
        return self.enabled

    def send_to_webhook(self, data: Dict[str, Any]) -> bool:
        """
        Envia dados ao webhook configurado do n8n.
        Retorna True em caso de sucesso, False em caso de erro.
        """
        if not self.is_enabled():
            logger.info("N8N_WEBHOOK_URL not configured or integration disabled.")
            return False  # Não é um erro, apenas não está habilitado

        try:
            response = requests.post(
                self.webhook_url,
                json=data,  # 'data' deve ser um dict serializável
                timeout=10
            )
            response.raise_for_status()  # Levanta HTTPError para respostas 4xx/5xx

            logger.info(f"Data sent to n8n webhook successfully. Status: {response.status_code}")
            return True  # Sucesso se não levantar exceção e código for 2xx

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"N8n webhook HTTP error: {http_err} - Response: {response.text}")
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"N8n webhook connection error: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            logger.error(f"N8n webhook timeout error: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            logger.error(f"N8n webhook request error: {req_err}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while sending data to n8n: {str(e)}")

        return False
