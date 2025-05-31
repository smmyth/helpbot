from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
from flask_cors import CORS
from config import app_config, TestConfig

mongo = PyMongo()
api = Api()
cors = CORS()

def create_app(config_object=app_config) -> Flask:
    """
    Fábrica de aplicação para criar e configurar a instância do Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Inicializar extensões com a app
    mongo.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Registrar rotas
    from .routes import register_routes
    register_routes(app)

    return app
