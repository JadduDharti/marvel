from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime


#Adding flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

#import secerets model (from python) generates a taken for each user
import secrets


#import flask login to check for an authentation user and store current user
from flask_login import UserMixin, LoginManager
#import flask marshmellow to help create our schemas
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    firstname = db.Column(db.String(150), nullable = True, default = '')
    lastname = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = True, default = '')
    username = db.Column(db.String(150), nullable = False)
    date_of_birth = db.Column(db.DateTime, nullable = True)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    def __init__(self, email, username, firstname = '', lastname = '', password = '', date_of_birth = ''):

        self.id = self.set_id()
        self.firstname = firstname
        self.lastname = lastname
        self.password = self.set_password(password)
        self.email = email
        self.username =username
        self.date_of_birth = date_of_birth
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f"User {self.email} has been added to the database..!"


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(500))
    comics_appeared_in = db.Column(db.Integer)
    super_power = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String, nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, comics_appeared_in, super_power, image_url, user_token):
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.image_url = image_url
        self.user_token = user_token


    def __repr__(self):
        return f'The following Hero has been added: {self.name}'

    def set_id(self):
        return str(uuid.uuid4())


# Creation of API Schema via the Marshmallow Object
# Character schema
class CharacterSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'comics_appeared_in', 'super_power', 'date_created', 'image_url')

# Initialize user and character schemas
character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)
