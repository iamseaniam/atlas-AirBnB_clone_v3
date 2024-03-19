#!/usr/bin/python3
""" Starts API """
from api.v1.views import app_views
from flask import Flask
from models import storage
import os
app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ Closes current SQLAlchemy session """
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
