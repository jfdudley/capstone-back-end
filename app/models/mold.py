from app import db

class Mold(db.Model):
    mold_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    well_shape = db.Column(db.String, nullable=False)
    well_volume_grams = db.Column(db.Integer, nullable=False)
    num_wells = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String, nullable=False)

    # Instance Methods

    def self_to_dict(self):
        instance_dict = dict(
            mold_id=self.mold_id,
            well_shape=self.well_shape,
            well_volume_grams=self.well_volume_grams,
            num_wells=self.num_wells,
            source=self.source
        )
        
        return instance_dict


    # Class methods

    @classmethod
    def return_class_name(cls):
        return cls.__name__

    @classmethod
    def create_from_dict(cls, data_dict):
        return cls(
            well_shape=data_dict["well_shape"],
            well_volume_grams=data_dict["well_volume_grams"],
            num_wells=data_dict["num_wells"],
            source=data_dict["source"]
        )