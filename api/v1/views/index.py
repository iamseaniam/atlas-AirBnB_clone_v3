#!/usr/bin/python3
"""Routes /status and /stats on object 'app_views'"""

from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route("/status")
def status_page():
    """Page declaring 'status': OK"""
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats_page():
    """Page relaying counts of each type of class objects"""
    cls_to_plural = {"amenities": Amenity, "cities": City, "places": Place,
                     "reviews": Review, "states": State, "users": User}
    cls_count_dict = {key: storage.count(cls) for key,
                      cls in cls_to_plural.items()}
    return jsonify(cls_count_dict)
