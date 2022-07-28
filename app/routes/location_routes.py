from flask import Blueprint, request, jsonify, make_response
from app.helper_functions import *
from app.models.location import Location
from app import db

location_bp = Blueprint("location_bp", __name__, url_prefix="/locations")
