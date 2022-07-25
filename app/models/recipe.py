from app import db

class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_name = db.Column(db.String, nullable=False)
    recipe_description = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    category = db.relationship("Category", back_populates='recipes')
    location_id = db.Column(db.Integer, db.ForeignKey('use_location.location_id'), nullable=False)
    use_location = db.relationship("Location", back_populates='recipes')
