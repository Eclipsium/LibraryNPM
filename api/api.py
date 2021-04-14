from flask import Blueprint

from .schema import BookSchema
from .service import BookService

book_bp = Blueprint('book_bp', __name__)


@book_bp.route("/", methods=['GET'])
def get_books() -> BookSchema:
    """Get all Books"""
    book_schema = BookSchema()
    books = BookService.get_all()
    return book_schema.dump(books)
