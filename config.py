import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jg0tgfh320-)x+=xq)*l)#*@opnl(!sy0z+6q=2ej4!&sqfbvc'


class DevelopmentConfig(Config):
    DEBUG = True
    username = os.getenv('POSTGRES_USER', 'postgres')
    password = os.getenv('POSTGRES_PASSWORD', 'recipeAppDB')
    hostname = os.getenv('POSTGRES_HOST', 'db')
    port = os.getenv('POSTGRES_PORT', '5432')
    database = os.getenv('POSTGRES_DB', 'recipe_app')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              f'postgresql://{username}:{password}@{hostname}:{port}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SERVER_NAME = 'localhost.localdomain'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # Disable CSRF tokens in the form

