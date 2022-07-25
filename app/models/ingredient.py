from app import db

class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient_name = db.Column(db.String, nullable=False)