from flask import Flask

from application.database import initialize_database
from application.models import User
from .auth import auth as auth_blueprint
from .main import main as main_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object('application.config.Config')
    initialize_database(app)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app


app = create_app()
