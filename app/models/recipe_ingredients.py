from app import db
from app.models.ingredient import Ingredient

class RecipeIngredients(db.Model):
    __tablename__ = "recipe_ingredients"
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True,nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.ingredient_id'), primary_key=True,nullable=False)
    percentage = db.Column(db.Integer, nullable=False)
    ingredients = db.relationship("Ingredient", back_populates="recipes")
    recipes = db.relationship("Recipe", back_populates="ingredients")


    def self_to_dict(self):
        instance_dict = dict(
            message="this is a recipe_ingredients instance",
            recipe_id = self.recipe_id,
            ingredient_id=self.ingredient_id,
            percentage=self.percentage
        )
        ingredient_list = self.ingredients.ingredient_name
        recipe_list = self.recipes.recipe_name

        instance_dict["ingredients_name"] = ingredient_list
        instance_dict["recipe_name"] = recipe_list

        return instance_dict