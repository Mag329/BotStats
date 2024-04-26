from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '0cf3cd9686c3b8ea8fa989ac1b0770983d910a9b'


db = SQLAlchemy(app)

app.app_context().push()

from app import models, routes

db.create_all()