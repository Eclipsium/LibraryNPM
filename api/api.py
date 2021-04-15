from flask import Blueprint, request
from marshmallow import ValidationError

from .models import Book
from .schema import BookSchema
from .service import BookService

book_bp = Blueprint('book_bp', __name__)
books_schema = BookSchema(many=True)
book_schema = BookSchema()


@book_bp.route("/book", methods=['GET'])
def get_books() -> books_schema:
    """Get all Books with limit"""
    limit = request.args.get('limit', default=None, type=int)

    books = BookService.get_all(limit)
    result = books_schema.dump(books)
    return {'status': 'success', 'message': result}, 200


@book_bp.route("/book", methods=['POST'])
def post_books() -> tuple:
    json_data = request.get_json()
    try:
        data = book_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422

    # Create new book
    book = BookService.create(data)
    if not book:
        return {"message": "Book with ISBN already exist"}, 409

    result = book_schema.dump(Book.query.get(book.book_id))
    return {"message": "Created new book.", "book": result}, 201


@book_bp.route("/book/<book_id>", methods=['GET'])
def detail_book(book_id) -> tuple:
    book = BookService.get_book_by_id(book_id)
    if book:
        result = book_schema.dump(book)
        return {"message": "Ok", "book": result}, 200
    else:
        return {"message": f"books with id {book_id} is not exist"}, 404


@book_bp.route("/book/<book_id>", methods=['PUT', 'PATCH'])
def update_book(book_id) -> tuple:
    json_data = request.get_json()
    try:
        data = book_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422

    book = BookService.get_book_by_id(book_id)
    if not book:
        return {"message": f"books with id {book_id} is not exist"}, 404

    isbn_id = BookService.get_id_by_isbn(data['isbn'])
    # Если isbn существует, и не совпадает с book_id
    if isbn_id and isbn_id != int(book_id):
        return {"message": f"books with isbn #{isbn_id} already exist"}, 409

    book = book_schema.load(json_data, instance=Book.query.get(book_id), partial=True)
    result = BookService.update(book)
    return {"message": "Ok", "book": book_schema.dump(result)}, 200


@book_bp.route("/book/<book_id>", methods=['DELETE'])
def delete_book(book_id) -> tuple:
    book = BookService.get_book_by_id(book_id)
    if not book:
        return {"message": f"books with id {book_id} is not exist"}, 404

    is_deleted = BookService.delete_by_id(book_id)
    if is_deleted:
        return {"message": "Ok"}, 204
    return {"message": "Something doing wrong"}, 500
