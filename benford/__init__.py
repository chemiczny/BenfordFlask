from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, makedirs

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    if test_config:
        app.config |= test_config

#    Session(app)
    db.init_app(app)
    if not path.isdir(app.config["UPLOAD_FOLDER"]):
        makedirs(app.config["UPLOAD_FOLDER"])

    with app.app_context():
        from .routes import home_bp
        app.register_blueprint(home_bp)
        db.create_all()

    return app
