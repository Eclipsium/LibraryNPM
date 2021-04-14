import os
from flask import Flask
from .api.api import book_bp
from .config import config_by_name
from . import db


flask_app = Flask(__name__)
flask_app.config.from_object(config_by_name[os.getenv("FLASK_ENV") or "test"])

db.init_app(flask_app)

with flask_app.app_context():
    db.create_all()

flask_app.register_blueprint(book_bp, url_prefix='/api', description='Operations on books')


if __name__ == "__main__":
    flask_app.run()
