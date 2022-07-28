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


# helper route for handling complex ingredient logic
def set_recipe_ingredients(recipe_record, ingredient_info):
    total_amount = 0
    for value in ingredient_info.values():
        total_amount += value

    for ingredient, amount in ingredient_info.items():
        ingredient_instance = get_or_create_record_by_name(Ingredient, ingredient, "ingredient_name")
        relation_instance = RecipeIngredients.query.filter_by(recipe_id=recipe_record.recipe_id, ingredient_id=ingredient_instance.ingredient_id).first()
        
        if amount == 0:
            db.session.delete(relation_instance)

        percentage = round((amount / total_amount) * 100)
        if not relation_instance:
            db.session.add(RecipeIngredients(recipe_id=recipe_record.recipe_id, ingredient_id=ingredient_instance.ingredient_id, percentage=percentage))
        else:
            setattr(relation_instance, "percentage", percentage)


# create new recipe, creating any new categories, locations, and ingredients along the way
@recipe_bp.route("", methods=["POST"])
def create_new_recipe():
    recipe_data = request.get_json()
    
    category = get_or_create_record_by_name(Category, recipe_data["category"], "category_name")
    location = get_or_create_record_by_name(Location, recipe_data["location"], "location_name")
    new_recipe = Recipe(
            recipe_name=recipe_data["recipe_name"], 
            recipe_description=recipe_data["recipe_description"],
            recipe_instructions=recipe_data["recipe_instructions"],
            category_id=category.category_id,
            location_id=location.location_id)
    db.session.add(new_recipe)

    set_recipe_ingredients(new_recipe, recipe_data["ingredient_info"])
    db.session.commit()

    return success_message_info(new_recipe.self_to_dict(), status_code=201)


# Update existing recipe by id
@recipe_bp.route("/<recipe_id>", methods=["PATCH"])
def update_recipe_by_id(recipe_id):
    update_data = request.get_json()
    recipe = get_record_by_id(Recipe, recipe_id)

    recipe_model_attributes = ["recipe_name", "recipe_description", "recipe_instructions"]

    for key in update_data.keys():
        if key in recipe_model_attributes:
            setattr(recipe, key, update_data[key])
        elif key == 'category':
            instance = get_or_create_record_by_name(Category, update_data[key], 'category_name')
            setattr(recipe, "category_id", instance.category_id)
        elif key == 'location':
            instance = get_or_create_record_by_name(Location, update_data[key], 'location_name')
            setattr(recipe, "location_id", instance.location_id)
        elif key == "ingredient_info":
            set_recipe_ingredients(recipe, update_data["ingredient_info"])

    db.session.commit()

    return success_message_info(recipe.self_to_dict(), status_code=200)


# Delete existing recipe by id
@recipe_bp.route("/<recipe_id>", methods=["DELETE"])
def delete_recipe_by_id(recipe_id):
    recipe = get_record_by_id(Recipe, recipe_id)

    for relation_instance in recipe.ingredients:
        db.session.delete(relation_instance)
    
    db.session.delete(recipe)
    db.session.commit()

    return success_message_info(f'Recipe {recipe.recipe_id} "{recipe.recipe_name}" successfully deleted', 200)
