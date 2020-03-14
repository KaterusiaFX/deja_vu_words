from app import app
from english_dict_generator import eng_dict_generator

with app.app_context():
    eng_dict_generator()
