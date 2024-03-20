#!/usr/bin/python3
"""Starts API"""
from flask import Flask, jsonify
from os import environ
from flask_cors import CORS
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes current SQLAlchemy session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = '0.0.0.0'
    port = environ.get('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
