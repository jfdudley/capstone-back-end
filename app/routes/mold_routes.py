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