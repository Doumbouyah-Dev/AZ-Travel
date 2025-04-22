from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config

# extensions

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    Migrate(app, db)

    with app.app_context():
        from . import routes, models  # noqa
        db.create_all()
    return app