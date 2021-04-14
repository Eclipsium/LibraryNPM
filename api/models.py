from sqlalchemy import Integer, Column, String
from .. import db


class Book(db.Model):
    """Some manual for Book model"""

    __tablename__ = "book"  # noqa

    book_id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(150))
    publisher = Column(String(100))
    genre = Column(String(100))
    page_count = Column(Integer())
    author = Column(String(100))
    isbn = Column(String(20), unique=True, index=True)

    def __repr__(self):
        return f'{self.title} - {self.ISBN}'
