import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db


'''
Extend the base Model class to add common methods
'''


class modelMethods(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


'''
Decks
These are the production intent products for Mooves.
Decks are collections of cards and are defined by a theme
(e.g. bodyweight, bootcamp, strength, endurance, ...)

'''


class Decks(modelMethods):
    __tablename__ = 'decks'

    id = Column(Integer, primary_key=True)
    code = Column(String)  # acronym for deck, eg. bodyweight = BW
    name = Column(String)
    theme = Column(String)
    description = Column(String)
    requisites = Column(String)

    def __init__(self, code="", name="", theme="", description="",
                 requisites=""):
        self.code = code
        self.name = name
        self.theme = theme
        self.description = description
        self.requisites = requisites

    def format(self):
        return {
          'id': self.id,
          'code': self.code,
          'name': self.name,
          'theme': self.theme,
          'description': self.description,
          'requisites': self.requisites
        }


'''
Exercises
Exercises are the building blocks for cards.
They are the literal exercises someone would do (eg. pushups).

'''


class Exercises(modelMethods):
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    prompt = Column(String)
    level = Column(Integer)

    def __init__(self, name="", prompt="", level=""):
        self.name = name
        self.prompt = prompt
        self.level = level

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'prompt': self.prompt,
          'level': self.level
        }


'''
Categories
Categories are groupings of exercies & cards by the muscle groups they target.

'''


class Categories(modelMethods):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    color = Column(String)  # hex color code

    def __init__(self, name="", color=""):
        self.name = name
        self.color = color

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'color': self.color
        }
