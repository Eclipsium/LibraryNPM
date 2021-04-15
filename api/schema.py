from .models import Book
from .. import ma, db


class BookSchema(ma.SQLAlchemyAutoSchema):
    """Widget schema"""

    class Meta:
        model = Book
        load_instance = True
        sqla_session = db.session # noqa
