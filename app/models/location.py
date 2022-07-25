from app import db

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String, nullable=False)
    recipes = db.relationship("Recipe", back_populates="use_location")