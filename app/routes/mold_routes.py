from flask import Blueprint, request, jsonify, make_response
from app.helper_functions import *
from app.models.mold import Mold
from app import db

# example_bp = Blueprint('example_bp', __name__)
mold_bp = Blueprint("mold_bp", __name__, url_prefix="/molds")

@mold_bp.route("", methods=["GET"])
def get_all_molds():
    molds = Mold.query.all()
    mold_response = [mold.self_to_dict() for mold in molds]
    return success_message_info(mold_response, status_code=200)


# get one mold by id 
@mold_bp.route("/<mold_id>", methods=["GET"])
def get_one_mold_by_id(mold_id):
    mold = get_record_by_id(Mold, mold_id)
    return success_message_info(mold.self_to_dict(), status_code=200)


@mold_bp.route("", methods=["POST"])
def create_new_mold():
    request_body = request.get_json()

    new_mold = create_record_safely(Mold, request_body)

    db.session.add(new_mold)
    db.session.commit()

    return success_message_info(new_mold.self_to_dict(), status_code=201)


# update mold info (change name) by id
@mold_bp.route("/<mold_id>", methods=["PATCH"])
def update_mold_by_id(mold_id):
    mold = get_record_by_id(Mold, mold_id)
    request_body = request.get_json()
    
    update_record_safely(Mold, mold, request_body)

    db.session.commit()

    return success_message_info(mold.self_to_dict(), status_code=200)


# Delete existing mold by id
@mold_bp.route("/<mold_id>", methods=["DELETE"])
def delete_mold_by_id(mold_id):
    mold = get_record_by_id(Mold, mold_id)
    
    db.session.delete(mold)
    db.session.commit()

    return success_message_info(f'Mold {mold.mold_id} "{mold.well_shape}" successfully deleted', 200)
