#!/usr/bin/python3
""" This script starts a Flask web application """
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from database.db_user import DBUser
from database import storage
from routes import app_views
from flasgger import Swagger
from flasgger.utils import swag_from


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown(self):
    """Removes the current SQLAlchemy Session"""
    return storage.close_db()


@app.errorhandler(404)
def error(e):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404
#print(DBUser.login(hola, mundo))

if __name__ == '__main__':
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True, debug=True)