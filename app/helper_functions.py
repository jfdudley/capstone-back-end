
from flask import jsonify, abort, make_response
import os
import requests

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def success_message_info(message, status_code=200):
    return make_response(jsonify(message), status_code)

def return_database_info_array(return_value):
    return make_response(jsonify(return_value))

def return_database_info_dict(category, return_value):
    return_dict = {}
    return_dict[category] = return_value
    return make_response(jsonify(return_dict))

def get_record_by_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id: {id}", 400)
    record = cls.query.get(id)
    if record:
        return record
    else:
        error_message(f"{cls.return_class_name()} id: {id} not found", 404)

def get_record_by_name(cls, name):
    if cls.return_class_name() == "Recipe":
        record = cls.query.filter_by(recipe_name = name).first()
    elif cls.return_class_name() == "Ingredient":
        record = cls.query.filter_by(ingredient_name = name).first()
    elif cls.return_class_name() == "Category":
        record = cls.query.filter_by(category_name = name).first()
    elif cls.return_class_name() == "Location":
        record = cls.query.filter_by(location_name = name).first()
    elif cls.return_class_name() == "Mold":
        record = cls.query.filter_by(mold_shape = name).first()
    else:
        record = None
    
    if record:
        return record
    else:
        error_message(f"{cls.return_class_name()} instance with name {name} not found", 404)

def create_record_safely(cls, data_dict):
    try:
        return cls.create_from_dict(data_dict)
    except ValueError as err:
        error_message(f"Invalid key(s): {err}.  {cls.return_class_name()} not added to {cls.return_class_name()} List.", 400)

def update_record_safely(cls, record, data_dict):
    try:
        update_self(record, data_dict)
    except ValueError as err:
        error_message(f"Invalid key(s): {err}. {cls.return_class_name()} not updated.", 400)

def update_self(instance, data_dict):
        dict_key_errors = []
        for key in data_dict.keys():
            if instance.hasattr(key):
                instance.setattr(key, data_dict[key])
            else:
                dict_key_errors.append(key)
        if dict_key_errors:
            raise ValueError(dict_key_errors)




