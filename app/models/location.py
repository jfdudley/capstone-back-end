from app import db

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String, nullable=False)
    recipes = db.relationship("Recipe", back_populates="location")

    required_attributes = {
        "location_name" : True,
    }

    # Instance Methods

    def self_to_dict(self, show_recipes=False):
        instance_dict = dict(
            location_id=self.location_id,
            location_name=self.location_name,
        )
        if show_recipes:
            instance_dict["recipes"] = [recipe.recipe_name for recipe in self.recipes] if self.recipes else []
        
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
                    location_name=data_dict["location_name"],
                )
            
        else:
            remaining_keys= set(data_dict.keys())-set(cls.required_attributes.keys())
            response=list(remaining_keys)
            raise ValueError(response)