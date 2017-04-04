# coding: utf-8
from flask import jsonify


def categories():
    return jsonify(
        [
            {'text': 'General', 'id': 'general'},
            {'text': 'Python', 'id': 'python'},
            {'text': 'News', 'id': 'news'},
        ]
    )


def configure(app):
    app.add_quokka_url_rule(
        '/quokka/ajax/categories',
        view_func=categories
    )
