from .users import User
from .oauth2 import OAuth2Token
from .questions import Question

from flask_mongoengine import MongoEngine

db = MongoEngine()

def init_db(app):
    db.init_app(app) 
