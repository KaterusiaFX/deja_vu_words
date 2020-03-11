from flask import Flask
from config import Config
from model import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

from app import routes
