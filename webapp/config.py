import os

# сюда вносить параметры конфигурации. Config - это общий класс для всех конфигураций


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'