# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - present bcstechnologies.com
"""

import os, json

from flask import Flask
from flask_cors import CORS
from .routes import rest_api
from .models import db
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        logging.FileHandler('app.log'),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)


logger = logging.getLogger(__name__)


app = Flask(__name__)

app.config.from_object('api.config.BaseConfig')

db.init_app(app)
rest_api.init_app(app)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['UPLOAD_FOLDER'] = 'static/pdfs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']

basedir = os.path.abspath(os.path.dirname(__file__))
upload_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
os.makedirs(upload_path, exist_ok=True)

# Setup database
@app.before_first_request
def initialize_database():
    """
    Initialize the database before the first request.
    If there is an exception with the primary database setup,
    it falls back to SQLite.
    """
    try:
        db.create_all()
    except Exception as e:

        print('> Error: DBMS Exception: ' + str(e) )

        # fallback to SQLite
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

        print('> Fallback to SQLite ')
        db.create_all()

@app.after_request
def after_request(response):
    """
    Sends back a custom error response with {"success", "msg"} format
    if the status code is 400 or higher.
    """
    if int(response.status_code) >= 400:
        try:
            response_data = response.get_data(as_text=True)
            logging.debug(f"Response data before parsing: {response_data}")
            response_data = json.loads(response_data)
            if "errors" in response_data:
                response_data = {"success": False,
                                 "msg": list(response_data["errors"].items())[0][1]}
        except ValueError as ve:
            logging.error(f"ValueError occurred: {ve}")
            response_data = {"success": False, "msg": "Unknown error occurred"}
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            response_data = {"success": False, "msg": str(e)}

        response.set_data(json.dumps(response_data))
        response.headers.add('Content-Type', 'application/json')
    return response