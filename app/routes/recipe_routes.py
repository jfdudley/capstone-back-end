from flask import Blueprint, request, jsonify, make_response
from app.helper_functions import *
from app.models.recipe import Recipe
from app.models.category import Category
from app.models.location import Location
from app.models.ingredient import Ingredient
from app.models.recipe_ingredients import RecipeIngredients
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


# create new recipe, creating any new categories, locations, and ingredients along the way
@recipe_bp.route("", methods=["POST"])
def create_new_recipe():
    recipe_data = request.get_json()
    
    category = get_or_create_record_by_name(Category, recipe_data["category"], "category_name")
    location = get_or_create_record_by_name(Location, recipe_data["location"], "location_name")
    new_recipe = Recipe(
            recipe_name=recipe_data["name"], 
            recipe_description=recipe_data["description"],
            recipe_instructions=recipe_data["instructions"],
            category_id=category.category_id,
            location_id=location.location_id)
    db.session.add(new_recipe)

    total_grams = 0
    for value in recipe_data["ingredients"].values():
        total_grams += value

    for ingredient, amount in recipe_data["ingredients"].items():
        percentage = round((amount / total_grams) * 100)
        ingredient_instance = get_or_create_record_by_name(Ingredient, ingredient, "ingredient_name")
        db.session.add(RecipeIngredients(recipe_id=new_recipe.recipe_id, ingredient_id=ingredient_instance.ingredient_id, percentage=percentage))
    
    db.session.commit()
    return success_message_info(new_recipe.self_to_dict(), status_code=201)
