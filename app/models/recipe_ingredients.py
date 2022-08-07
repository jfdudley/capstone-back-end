from app import db
from app.models.ingredient import Ingredient

class RecipeIngredients(db.Model):
    __tablename__ = "recipe_ingredients"
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True,nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.ingredient_id'), primary_key=True,nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    ingredient = db.relationship("Ingredient", back_populates="recipes")
    recipe = db.relationship("Recipe", back_populates="ingredients")


    # Instance Methods 

    def self_to_dict(self, perspective):
        if perspective == 'recipe':
            instance_dict = dict(
                ingredient_id=self.ingredient_id,
                ingredient_name=self.ingredient.ingredient_name,
                percentage=self.percentage
            )
        if perspective == 'ingredient':
            instance_dict = dict(
                recipe_id=self.recipe_id,
                recipe_name=self.recipe.recipe_name,
                percentage=self.percentage
            )

        return instance_dict
    
    # Class Methods

    @classmethod
    def return_class_name(cls):
        return cls.__name__

    # No create_from_dict class method because creating a new recipe record requires instances of other models
