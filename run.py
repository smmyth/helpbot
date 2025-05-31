"""
Arquivo principal para inicialização da aplicação HelpBot (Flask).
"""

import logging

# Configuração global de logging (pode customizar o formato, nível etc)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

from app import create_app
from config import app_config

app = create_app(app_config)

if __name__ == '__main__':
    logging.info("Iniciando a aplicação HelpBot...")
    app.run(host='0.0.0.0', port=5000, debug=app_config.DEBUG)
