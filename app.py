import os
from flask import Flask
from .api.api import book_bp
from .config import config_by_name
from . import db

flask_app = Flask(__name__)
sys_env = os.getenv("FLASK_ENV")  # development, test, production

if sys_env:
    config = config_by_name[sys_env]
else:
    config = config_by_name["test"]

flask_app.config.from_object(config)

db.init_app(flask_app)

with flask_app.app_context():
    db.create_all()

flask_app.register_blueprint(book_bp, url_prefix='/api', description='Operations with books')

if __name__ == "__main__":
    flask_app.run()
