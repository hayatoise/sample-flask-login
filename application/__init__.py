from flask import Flask

from application.database import initialize_database
from application.models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object('application.config.Config')
    initialize_database(app)

    return app


app = create_app()
