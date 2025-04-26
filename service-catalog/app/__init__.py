from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# initialize the database and migration objects
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    db.init_app(app)
    migrate.init_app(app, db)

    # import the model
    from .models import CakeCatalog 

    return app