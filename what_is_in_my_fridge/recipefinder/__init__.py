from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Creating basic flask web app with sqlite database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'     
db = SQLAlchemy(app)

from recipefinder import routes