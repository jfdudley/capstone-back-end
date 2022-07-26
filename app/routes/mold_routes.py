from flask import Blueprint, request, jsonify, make_response
from app.helper_functions import *
from app import db

# example_bp = Blueprint('example_bp', __name__)
mold_bp = Blueprint("mold_bp", __name__, url_prefix="/molds")
