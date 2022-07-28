from app import db

class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient_name = db.Column(db.String, nullable=False)
    recipes = db.relationship("RecipeIngredients", back_populates="ingredient")


    # Instance Methods

    def self_to_dict(self, show_recipes=False):
        instance_dict = dict(
            ingredient_id = self.ingredient_id,
            ingredient_name=self.ingredient_name
        )
        if show_recipes:
            recipe_info = [recipe.self_to_dict("ingredient") for recipe in self.recipes] if self.recipes else []
            instance_dict["recipe_info"] = recipe_info
        
        return instance_dict


    # Class methods

    @classmethod
    def return_class_name(cls):
        return cls.__name__

    @classmethod
    def create_from_dict(cls, data_dict):
        return cls(ingredient_name=data_dict["ingredient_name"])