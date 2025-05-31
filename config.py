import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """
    Configurações base da aplicação Flask, carregadas de variáveis de ambiente.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'uma-chave-secreta-padrao-muito-segura')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/helpbot')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    # Configurações para OpenAI
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', 0.7))
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', 150))


class DevelopmentConfig(Config):
    """
    Configurações específicas de desenvolvimento.
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Configurações específicas de produção.
    """
    DEBUG = False
    # Outras configurações específicas de produção (ex: logging mais robusto)


class TestConfig(Config):
    """
    Configurações para ambiente de testes automatizados.
    """
    TESTING = True
    DEBUG = True
    MONGO_URI = os.getenv('TEST_MONGO_URI', 'mongodb://localhost:27017/helpbot_test')
    # Garante que APIs externas não sejam chamadas durante testes, se necessário
    OPENAI_API_KEY = None  # Ou uma chave de teste mock
    N8N_WEBHOOK_URL = None  # Ou um endpoint de teste mock

# Mapeamento para facilitar a seleção da configuração via FLASK_ENV
config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
    testing=TestConfig
)

# Exporta a configuração baseada em FLASK_ENV ou padrão para desenvolvimento
flask_env = os.getenv('FLASK_ENV', 'development')
app_config = config_by_name.get(flask_env, DevelopmentConfig)
