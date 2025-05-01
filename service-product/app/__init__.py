from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# import the config file
from config import Config

# initialize the database and migration objects
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # import the model
    from .models.model import Products

    from .resources import create_api_blueprint

    # register the api blueprint
    app.register_blueprint(create_api_blueprint(db), url_prefix='/api/v1')

    return app