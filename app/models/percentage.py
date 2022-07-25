from app import db

class Percentage(db.Model):
    percent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    percent_amount = db.Column(db.Float, nullable=False)