from app import db

class Mold(db.Model):
    mold_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    well_shape = db.Column(db.String, nullable=False)
    well_volume = db.Column(db.Integer, nullable=False)
    num_wells = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String)
