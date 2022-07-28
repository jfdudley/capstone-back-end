from flask import Blueprint, request, jsonify, make_response
from app.helper_functions import *
from app.models.location import Location
from app import db

location_bp = Blueprint("location_bp", __name__, url_prefix="/locations")

# no POST route as new locations can only be created with the creation of a recipe

# get all locations
@location_bp.route("", methods=["GET"])
def get_all_locations():
    locations = Location.query.all()
    location_response = [location.self_to_dict() for location in locations]
    return success_message_info(location_response, status_code=200)


# get one location by id 
@location_bp.route("/<location_id>", methods=["GET"])
def get_one_location_no_recipe_info(location_id):
    location = get_record_by_id(Location, location_id)
    return success_message_info(location.self_to_dict(), status_code=200)


@location_bp.route("/<location_id>/recipes", methods=["GET"])
def get_one_location_with_recipe_info(location_id):
    location = get_record_by_id(Location, location_id)
    return success_message_info(location.self_to_dict(show_recipes=True), status_code=200)


# update location info (change name) by id
@location_bp.route("/<location_id>", methods=["PATCH"])
def update_location(location_id):
    location = get_record_by_id(Location, location_id)
    request_body = request.get_json()
    if "recipes" in request_body:
        return error_message("Recipe-location relationships may only be updated from recipe records.", 405)

    update_record_safely(Location, location, request_body)

    db.session.commit()

    return success_message_info(location.self_to_dict(), status_code=200)


# Delete existing location by id
@location_bp.route("/<location_id>", methods=["DELETE"])
def delete_location_by_id(location_id):
    location = get_record_by_id(Location, location_id)

    location_info = location.self_to_dict(show_recipes=True)

    if location_info["recipes"]:
        return error_message("Location record is in use and so cannot be deleted.", 405)
    
    db.session.delete(location)
    db.session.commit()

    return success_message_info(f'Location {location.location_id} "{location.location_name}" successfully deleted', 200)
