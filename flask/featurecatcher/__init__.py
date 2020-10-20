from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    db.init_app(app)
    from . import models

    # blueprint
    from .views import main_views
    app.register_blueprint(main_views.bp)
    
    return app
