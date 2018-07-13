from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e4efa3e6d190179a7d2daacbf6790fdf'

from flasktools import routes