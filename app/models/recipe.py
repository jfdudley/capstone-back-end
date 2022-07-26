from app import db

class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_name = db.Column(db.String, nullable=False)
    recipe_description = db.Column(db.String, nullable=False)
    recipe_instructions = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    category = db.relationship("Category", back_populates='recipes')
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    location = db.relationship("Location", back_populates='recipes')
    ingredients = db.relationship("RecipeIngredients", back_populates="recipes")

    # Instance Methods

    def self_to_dict(self):
        instance_dict = dict(
            recipe_name=self.recipe_name,
            recipe_description=self.recipe_description,
            category=self.category.category_name,
            use_location=self.location.location_name,
        )
        # instructions should be long string with line breaks before each next step
        # ex: "1. Melt waxes, butters, and oils together over low heat\n2. When liquid, remove from heat and let cool slightly\n3....."
        # code below splits string into a list of string values
        instructions_list = self.recipe_instructions.splitlines()

        instance_dict["instructions"] = instructions_list

        ingredient_info = [ingredient.self_to_dict() for ingredient in self.ingredients] if self.ingredients else []

        instance_dict["ingredient_info"] = ingredient_info

        # Need to add stuff here about getting ingredients and amounts - stored as nested dictionary?

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
    
    # Class Methods

    @classmethod
    def return_class_name(cls):
        return cls.__name__

    # No create_from_dict class method because creating a new recipe record requires instances of other models
