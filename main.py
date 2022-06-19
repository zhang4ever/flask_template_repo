from flask import  Flask

from config import flask_config
from app.controller import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(flask_config)
    register_blueprints(app)

    return app
