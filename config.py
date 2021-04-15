import os
from typing import List, Type

from sqlalchemy.engine import URL

from .db_setting import DATABASE

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    CONFIG_NAME = "base"
    FLASK_DEBUG = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = URL(**DATABASE)


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "dev"
    SECRET_KEY = os.getenv(
        "DEV_SECRET_KEY", "NPM это не пакетный менеджер Node.js, а компания, которая меня рекрутит :D"
    )
    FLASK_DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    SECRET_KEY = os.getenv("TEST_SECRET_KEY", "Если сразу не получилось хорошо, назовите это версией 1.0")
    FLASK_DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    CONFIG_NAME = "prod"
    SECRET_KEY = os.getenv("PROD_SECRET_KEY", "Чтобы понять рекурсию, нужно сперва понять рекурсию.")
    FLASK_DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "some prod url"


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]
config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
