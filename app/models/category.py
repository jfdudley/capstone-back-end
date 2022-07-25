from app import db

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String, nullable=False)
    recipes = db.relationship("Recipe", back_populates="category")

