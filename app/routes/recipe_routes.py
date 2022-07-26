from flask import Blueprint, request, jsonify, make_response
from app.helper_functions import *
from app.models.recipe import Recipe
from app import db

# example_bp = Blueprint('example_bp', __name__)
recipe_bp = Blueprint("recipe_bp", __name__, url_prefix="/recipes")

@recipe_bp.route("", methods=["GET"])
def get_boards():
    recipes = Recipe.query.all()
    recipe_response = [recipe.self_to_dict() for recipe in recipes]
    return success_message_info_as_list(recipe_response, status_code=200)