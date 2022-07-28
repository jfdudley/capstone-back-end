from app import db

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String, nullable=False)
    recipes = db.relationship("Recipe", back_populates="category")


    # Instance Methods

    def self_to_dict(self, show_recipes=False):
        instance_dict = dict(
            category_id=self.category_id,
            category_name=self.category_name,
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
        return cls(category_name=data_dict["category_name"])
