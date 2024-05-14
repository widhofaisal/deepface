from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

from flask_cors import CORS
from app.config import Config

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

app.config.from_object(Config)
app.logger.setLevel(logging.INFO)
db = SQLAlchemy(app)

from app import routes, models
