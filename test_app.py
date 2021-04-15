from . import db
from .api.models import Book
from .app import flask_app


class TestBase:
    def insert_db(self):
        books_data = {
            'title': ['1001 ночь', 'Молчание ягнят', 'Философия Java'],
            'publisher': ['Глобус', '1C', 'For only'],
            'genre': ['Сказки', 'Триллер', 'Самоучитель'],
            'page_count': ['152', '543', '1305'],
            'author': ['Джон Сноу', 'Джонатан Демми', 'Билл Гейтс'],
            'isbn': ['2-266-11156-6', '3-266-11156-6', '2-266-11156-4'],
        }
        for index in range(3):
            new_book = Book(
                book_id=index,
                title=books_data['title'][index],
                publisher=books_data['publisher'][index],
                genre=books_data['genre'][index],
                page_count=books_data['page_count'][index],
                author=books_data['author'][index],
                isbn=books_data['isbn'][index]
            )
            with self.app.app_context():
                db.session.add(new_book)
                db.session.commit()

    def setup(self):
        self.app = flask_app  # noqa
        self.client = self.app.test_client()  # noqa

        with self.app.app_context():
            Book.query.delete()
            db.session.commit()

        self.insert_db()

    def teardown(self):
        with self.app.app_context():
            Book.query.delete()
            db.session.commit()


class TestUrl(TestBase):
    def test_urls(self):
        # wrong url
        assert self.client.get('/').status_code == 404
        assert self.client.get('api/book/').status_code == 404

        # success url
        assert self.client.get('api/book/1').status_code == 200
        assert self.client.get('api/book').status_code == 200

        # check available http methods
        assert self.client.post('api/book/1').status_code == 405
        assert self.client.delete('api/book/').status_code == 404

        # put with empty body
        assert self.client.put('api/book/1').status_code == 422


class TestApi(TestBase):
    payload = {
        'title': 'Толстый питон',
        'publisher': 'O-really',
        'genre': 'Самоучитель',
        'page_count': 400,
        'author': 'Ник Джонсон',
        'isbn': '2-266-11656-4',
    }

    def test_get_books(self):
        book_data = self.client.get('api/book/4').json
        assert book_data == {'message': 'books with id 4 is not exist'}

        book_data = self.client.get('api/book').json
        assert book_data['status'] == 'success'
        assert len(book_data['message']) == 3

    def test_create_books(self):
        assert self.client.post('api/book', json=self.payload).status_code == 201

    def test_create_book_with_exist_isbn(self):
        self.payload['isbn'] = '2-266-11156-6'  # 1001 ночь
        assert self.client.post('api/book', json=self.payload).status_code == 409

    def test_create_book_with_bad_data(self):
        self.payload['title'] = 123123  # must be str
        assert self.client.post('api/book', json=self.payload).status_code == 422

    def test_delete_book(self):
        assert self.client.delete('api/book/1').status_code == 204
