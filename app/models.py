import secrets

from app import db, app
from flask_login import UserMixin, LoginManager


login = LoginManager(app)
login.login_view = 'login'
login.login_message = ''

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    
    
class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False, default='online')
    

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text, nullable=False)
    data = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.Text, nullable=False)
    
    
def generate_token():
    token = secrets.token_urlsafe(24)
    return token


def check_token(token):
    bot = Bot.query.filter_by(token=token).first()
    if bot:
        return True
    return False