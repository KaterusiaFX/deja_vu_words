from model import db
from app import app

db.create_all(app=app)