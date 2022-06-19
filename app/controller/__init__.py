from flask import Flask

from app.controller.health_check import check


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(check)