import os
from decouple import config
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SESSION_TYPE = 'filesystem'
    RESULTS_PER_PAGE = 5
    FLASK_DEBUG = 1
    # debug = True
    TEMPLATES_AUTO_RELOAD = True
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = config("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = os.path.join(basedir, 'app/static')

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') \
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    DEBUG=True
    SQLALCHEMY_ECHO=True

class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass