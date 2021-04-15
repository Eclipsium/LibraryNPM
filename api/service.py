from typing import List, Any

from sqlalchemy.orm import load_only

from .. import db

from .models import Book
from .schema import BookSchema


class BookService:
    @staticmethod
    def get_all(limit) -> List[Book]:
        return Book.query.limit(limit).all()

    @staticmethod
    def get_book_by_id(book_id: int) -> Book:
        return Book.query.get(book_id)

    @staticmethod
    def get_id_by_isbn(book_isbn) -> int:
        book = Book.query.filter_by(isbn=book_isbn).options(load_only('book_id')).first()
        return int(book.book_id) if book else 0

    @staticmethod
    def update(book: Book) -> Book:
        db.session.commit()
        return book

    @staticmethod
    def create(params: BookSchema) -> Book:
        new_book = Book(
            title=params["title"],
            publisher=params["publisher"],
            genre=params["genre"],
            page_count=params["page_count"],
            author=params["author"],
            isbn=params["isbn"]
        )
        if BookService.get_id_by_isbn(params['isbn']):
            return None  # noqa
        db.session.add(new_book)
        db.session.commit()

        return new_book

    @staticmethod
    def delete_by_id(book_id: int) -> bool:
        book = Book.query.filter(Book.book_id == book_id).first()
        if not book:
            return False
        db.session.delete(book)
        db.session.commit()
        return True
