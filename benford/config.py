from os import path
basedir = path.abspath(path.dirname(__file__))

UPLOAD_FOLDER = 'UPLOADS'

SECRET_KEY = '2ed56fa3a05a5d83919f6a88b8cdf8a8'

SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, "analysis.db")
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
