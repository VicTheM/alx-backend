#!/usr/bin/env python3
"""Basic Flask Application"""
from flask import Flask, request, render_template
from flask_babel import Babel


class Config():
    """Configures the app"""

    LANGUAGES = ['en', 'fr']

    def __init__(self):
        pass

@babel.localeselector
def get_locale():
    """Gets the current language to use"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


app = Flask(__name__)
babel = Babel(app, locale_selector=get_locale)


@app.route('/')
def index():
    """Index page"""
    return render_template('1-index.html')
