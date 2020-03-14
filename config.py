import os

basedir = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(basedir, 'deja_vu_database.db')

# сюда вносить параметры конфигурации. Config - это общий класс для всех конфигураций
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_DIR}' 
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
