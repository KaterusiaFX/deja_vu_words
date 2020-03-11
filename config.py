import os

basedir = os.path.abspath(os.path.dirname(__file__))

# сюда вносить параметры конфигурации. Config - это общий класс для всех конфигураций
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'word_dict.db')
