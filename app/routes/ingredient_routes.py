from flask import Blueprint, request
from app.helper_functions import *
from app.models.ingredient import Ingredient
from app import db

ingredient_bp = Blueprint("ingredient_bp", __name__, url_prefix="/ingredients")


# no POST route as new ingredients can only be created with the creation of a recipe

# get all ingredients
@ingredient_bp.route("", methods=["GET"])
def get_all_ingredients():
    ingredients = Ingredient.query.all()
    ingredient_response = [ingredient.self_to_dict() for ingredient in ingredients]
    return success_message_info(ingredient_response, status_code=200)


# get one ingredient by id 
@ingredient_bp.route("/<ingredient_id>", methods=["GET"])
def get_one_ingredient_no_recipe_info(ingredient_id):
    ingredient = get_record_by_id(Ingredient, ingredient_id)
    return success_message_info(ingredient.self_to_dict(), status_code=200)


@ingredient_bp.route("/<ingredient_id>/recipes", methods=["GET"])
def get_one_ingredient_with_recipe_info(ingredient_id):
    ingredient = get_record_by_id(Ingredient, ingredient_id)
    return success_message_info(ingredient.self_to_dict(show_recipes=True), status_code=200)


# update ingredient info (change name) by id
@ingredient_bp.route("/<ingredient_id>", methods=["PATCH"])
def update_ingredient(ingredient_id):
    ingredient = get_record_by_id(Ingredient, ingredient_id)
    request_body = request.get_json()
    if "recipe_info" in request_body:
        return error_message("Recipe-ingredient relationships may only be updated from recipe records.", 405)

    update_record_safely(Ingredient, ingredient, request_body)

    db.session.commit()

    return success_message_info(ingredient.self_to_dict(), status_code=200)


# Delete existing ingredient by id
@ingredient_bp.route("/<ingredient_id>", methods=["DELETE"])
def delete_ingredient_by_id(ingredient_id):
    ingredient = get_record_by_id(Ingredient, ingredient_id)

    ingredient_info = ingredient.self_to_dict(show_recipes=True)

    if ingredient_info["recipe_info"]:
        return error_message("Ingredient record is in use and so cannot be deleted.", 405)
    
    db.session.delete(ingredient)
    db.session.commit()

    return success_message_info(f'Ingredient {ingredient.ingredient_id} "{ingredient.ingredient_name}" successfully deleted', 200)
