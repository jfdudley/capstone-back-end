
from flask import jsonify, abort, make_response
import os
import requests
from app import db


def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def success_message_info(message, status_code=200):
    return make_response(jsonify(message), status_code)

def get_record_by_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id: {id}", 400)
    record = cls.query.get(id)
    if record:
        return record
    else:
        error_message(f"{cls.return_class_name()} id: {id} not found.", 404)

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
    return record

def create_record_safely(cls, data_dict):
    return cls.create_from_dict(data_dict)

def update_record_safely(cls, record, data_dict):
    try:
        update_self(record, data_dict)
    except ValueError as err:
        error_message(f"Invalid key(s): {err}. {cls.return_class_name()} not updated.", 400)
    # updating record is maintaining error handling where create record is not
    # because create record will be handled by forms on the front end and so data_dict keys will always be correct
    # updating a record may remain accessible via postman only and so should protect against human error

def update_self(instance, data_dict):
        dict_key_errors = []
        for key in data_dict.keys():
            if hasattr(instance, key):
                setattr(instance, key, data_dict[key])
            else:
                dict_key_errors.append(key)
        if dict_key_errors:
            raise ValueError(dict_key_errors)

def get_or_create_record_by_name(cls, new_value, cls_attribute):
    instance = get_record_by_name(cls, new_value)
    if not instance:
        instance = create_record_safely(cls, {cls_attribute : new_value})
        db.session.add(instance)
        db.session.commit()
    return instance




