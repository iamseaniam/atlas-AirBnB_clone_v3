#!/usr/bin/python3
""" Routes /status on object 'app_views' and returns JSON status """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_api_status():
    return jsonify({"status": "OK"})
