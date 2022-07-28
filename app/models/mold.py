from app import db

class Mold(db.Model):
    mold_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    well_shape = db.Column(db.String, nullable=False)
    well_volume_grams = db.Column(db.Integer, nullable=False)
    num_wells = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String, nullable=False)

    required_attributes = {
        "well_shape" : True,
        "well_volume_grams" : True,
        "num_wells" : True,
        "source" : True
    }

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

    def update_self(self, data_dict):
        dict_key_errors = []
        for key in data_dict.keys():
            if hasattr(self, key):
                setattr(self, key, data_dict[key])
            else:
                dict_key_errors.append(key)
        if dict_key_errors:
            raise ValueError(dict_key_errors)

    # Class methods

    @classmethod
    def return_class_name(cls):
        return cls.__name__

    @classmethod
    def create_from_dict(cls, data_dict):
        if data_dict.keys() == cls.required_attributes.keys():
                return cls(
                    well_shape=data_dict["well_shape"],
                    well_volume_grams=data_dict["well_volume_grams"],
                    num_wells=data_dict["num_wells"],
                    source=data_dict["source"]
                )
            
        else:
            remaining_keys= set(data_dict.keys())-set(cls.required_attributes.keys())
            response=list(remaining_keys)
            raise ValueError(response)