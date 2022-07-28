from app import db

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String, nullable=False)
    recipes = db.relationship("Recipe", back_populates="location")


    # Instance Methods

    def self_to_dict(self, show_recipes=False):
        instance_dict = dict(
            location_id=self.location_id,
            location_name=self.location_name,
        )
        if show_recipes:
            instance_dict["recipes"] = [recipe.recipe_name for recipe in self.recipes] if self.recipes else []
        
        return instance_dict


    # Class methods

    @classmethod
    def return_class_name(cls):
        return cls.__name__

    @classmethod
    def create_from_dict(cls, data_dict):
        return cls(location_name=data_dict["location_name"])