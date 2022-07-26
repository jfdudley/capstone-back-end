from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    from app.models.mold import Mold
    from app.models.category import Category
    from app.models.location import Location
    from app.models.recipe import Recipe
    from app.models.ingredient import Ingredient
    from app.models.recipe_ingredients import RecipeIngredients

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes.recipe_routes import recipe_bp
    app.register_blueprint(recipe_bp)

    CORS(app)
    return app
