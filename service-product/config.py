import os

class Config:
    DEBUG = False
    Testing = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:johancar12@localhost:3306/prueba_microservicios'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class developmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    Testing = True

class productionConfig(Config):
    DEBUG = False
    Testing = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')