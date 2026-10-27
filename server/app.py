#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")

DEFAULT_PER_PAGE = 5
MAX_PER_PAGE = 100

class Books(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', DEFAULT_PER_PAGE, type=int)

        page = max(page, 1)
        per_page = min(max(per_page, 1), MAX_PER_PAGE)

        pagination = Book.query.order_by(Book.id).paginate(
            page=page, per_page=per_page, error_out=False)

        return {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'total_pages': pagination.pages,
            'items': [BookSchema().dump(book) for book in pagination.items],
        }, 200

api.add_resource(Books, '/books', endpoint='books')

app = create_app(env)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

