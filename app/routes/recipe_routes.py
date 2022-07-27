from flask import Blueprint, request, jsonify, make_response
from app.helper_functions import *
from app.models.recipe import Recipe
from app import db

recipe_bp = Blueprint("recipe_bp", __name__, url_prefix="/recipes")

# get all recipes
@recipe_bp.route("", methods=["GET"])
def get_all_recipes():
    recipes = Recipe.query.all()
    recipe_response = [recipe.self_to_dict() for recipe in recipes]
    return success_message_info(recipe_response, status_code=200)


# get one recipe by id
@recipe_bp.route("/<recipe_id>", methods=["GET"])
def get_one_recipe(recipe_id):
    recipe = get_record_by_id(Recipe, recipe_id)
    return success_message_info(recipe.self_to_dict(), status_code=200)

