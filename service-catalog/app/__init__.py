from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# import the api blueprint
from .resources import api_bp
# import the config file
from config import Config

# initialize the database and migration objects
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    db.init_app(app)
    migrate.init_app(app, db)

    # import the model
    from .models.model import CakeCatalog 

    # register the api blueprint
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app