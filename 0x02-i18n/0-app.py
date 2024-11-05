#!/usr/bin/env python3
"""Basic Flask Application"""
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    """Index page"""
    return render_template('0-index.html')
