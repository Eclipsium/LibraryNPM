import os
from typing import List, Type

from sqlalchemy.engine import URL
from .db_setting import DATABASE, TEST_DATABASE

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    CONFIG_NAME = "base"
    ENV = 'development'
    FLASK_DEBUG = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = URL.create(**DATABASE)


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "development"
    SECRET_KEY = os.getenv(
        "DEV_SECRET_KEY", "NPM это не пакетный менеджер Node.js, а компания, которая меня рекрутит :D"
    )
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    SECRET_KEY = os.getenv("TEST_SECRET_KEY", "Если сразу не получилось хорошо, назовите это версией 1.0")
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = URL.create(**TEST_DATABASE)


class ProductionConfig(BaseConfig):
    CONFIG_NAME = "production"
    ENV = 'production'
    SECRET_KEY = os.getenv("PROD_SECRET_KEY", "Чтобы понять рекурсию, нужно сперва понять рекурсию.")
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "some prod url"


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
]
config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
