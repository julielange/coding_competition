from recipefinder import db
from datetime import datetime
from sqlalchemy import ForeignKey


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredients = db.Column(db.String(120), nullable=False)
    date =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recipe = db.relationship('Recipe', backref='search', lazy=True)

    def __repr__(self):
        return 'Request ' + str(self.id)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    title = db.Column(db.String(120))
    image = db.Column(db.String(240))
    favourite = db.Column(db.Boolean, default=False)
    search_id = db.Column(db.Integer, db.ForeignKey('search.id'))
    instructions = db.relationship("Instructions", backref='recipe', lazy=True)

    def __repr__(self):
        return 'Recipe ' + str(self.id)


class Instructions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.String)
    step_no = db.Column(db.Integer)
    recipe_id = db.Column(db.Integer, ForeignKey('recipe.id'))

    def __repr__(self):
        return 'Instruction ' + str(self.id)


class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String(120))
    amount = db.Column(db.String(240))
    unit = db.Column(db.String(120))

    def __repr__(self):
        return 'Ingredient ' + str(self.id)
