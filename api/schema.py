from .models import Book
from .. import ma


class BookSchema(ma.SQLAlchemyAutoSchema):
    """Widget schema"""

    class Meta:
        model = Book
