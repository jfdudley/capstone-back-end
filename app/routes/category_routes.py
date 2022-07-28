from flask import Blueprint, request, jsonify, make_response
from app.helper_functions import *
from app.models.category import Category
from app import db

category_bp = Blueprint("category_bp", __name__, url_prefix="/categories")

# no POST route as new categories can only be created with the creation of a recipe

# get all categories
@category_bp.route("", methods=["GET"])
def get_all_categories():
    categories = Category.query.all()
    category_response = [category.self_to_dict() for category in categories]
    return success_message_info(category_response, status_code=200)


# get one category by id 
@category_bp.route("/<category_id>", methods=["GET"])
def get_one_category_no_recipe_info(category_id):
    category = get_record_by_id(Category, category_id)
    return success_message_info(category.self_to_dict(), status_code=200)


@category_bp.route("/<category_id>/recipes", methods=["GET"])
def get_one_category_with_recipe_info(category_id):
    category = get_record_by_id(Category, category_id)
    return success_message_info(category.self_to_dict(show_recipes=True), status_code=200)


# update category info (change name) by id
@category_bp.route("/<category_id>", methods=["PATCH"])
def update_category(category_id):
    category = get_record_by_id(Category, category_id)
    request_body = request.get_json()
    if "recipes" in request_body:
        return error_message("Recipe-category relationships may only be updated from recipe records.", 405)

    update_record_safely(Category, category, request_body)

    db.session.commit()

    return success_message_info(category.self_to_dict(), status_code=200)


# Delete existing category by id
@category_bp.route("/<category_id>", methods=["DELETE"])
def delete_category_by_id(category_id):
    category = get_record_by_id(Category, category_id)

    category_info = category.self_to_dict(show_recipes=True)

    if category_info["recipes"]:
        return error_message("Category record is in use and so cannot be deleted.", 405)
    
    db.session.delete(category)
    db.session.commit()

    return success_message_info(f'Category {category.category_id} "{category.category_name}" successfully deleted', 200)
