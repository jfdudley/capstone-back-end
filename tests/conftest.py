import pytest
from app import create_app
from app import db
from app.models.category import Category
from app.models.ingredient import Ingredient
from app.models.location import Location
from app.models.mold import Mold
from app.models.recipe_ingredients import RecipeIngredients
from app.models.recipe import Recipe


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def three_categories(app):
    category_1 = Category(category_name="Moisturizer")
    category_2 = Category(category_name="Cleanser")
    category_3 = Category(category_name="Scrub")

    db.session.add_all([category_1, category_2, category_3])
    db.session.commit()

@pytest.fixture
def three_locations(app):
    location_1 = Location(location_name="Body")
    location_2 = Location(location_name="Face")
    location_3 = Location(location_name="Lips")

    db.session.add_all([location_1, location_2, location_3])
    db.session.commit()

@pytest.fixture
def nine_ingredients(app):
    ingredients = [
        Ingredient(ingredient_name="Beeswax"),
        Ingredient(ingredient_name="Rice Bran Wax"),
        Ingredient(ingredient_name="Cetyl Alcohol"),
        Ingredient(ingredient_name="Shea Butter"),
        Ingredient(ingredient_name="Cocoa Butter"),
        Ingredient(ingredient_name="Mango Butter"),
        Ingredient(ingredient_name="Almond Oil"),
        Ingredient(ingredient_name="Jojoba Oil"),
        Ingredient(ingredient_name="Argan Oil")
    ]

    db.session.add_all(ingredients)
    db.session.commit()

@pytest.fixture
def one_recipe(app, three_categories, three_locations, nine_ingredients):
    category = Category.query.get(1)
    location = Location.query.get(1)
    recipe = Recipe(
        recipe_name="Basic Solid Lotion", 
        recipe_description="A basic solid lotion recipe",
        recipe_instructions="1. Melt wax, butter, and oil together\n2. Remove from heat and cool slightly\n3. Pour into mold and cool overnight until solid",
        category_id=category.category_id,
        location_id=location.location_id)
    db.session.add(recipe)
    
    wax = Ingredient.query.get(1) # should be beeswax
    butter = Ingredient.query.get(4) # should be shea butter
    oil = Ingredient.query.get(7) # should be almond oil

    db.session.add(RecipeIngredients(recipe_id=1, ingredient_id=wax.ingredient_id, percentage=33))
    db.session.add(RecipeIngredients(recipe_id=1, ingredient_id=butter.ingredient_id, percentage=33))
    db.session.add(RecipeIngredients(recipe_id=1, ingredient_id=oil.ingredient_id, percentage=33))
    db.session.commit()

@pytest.fixture
def three_recipes(app, three_categories, three_locations, nine_ingredients):
    for i in range(3):
        num = i + 1
        category = Category.query.get(num)
        location = Location.query.get(num)
        recipe = Recipe(
            recipe_name=f"Basic Solid {category.category_name}", 
            recipe_description=f"A basic solid {category.category_name} recipe",
            recipe_instructions=f"1. Melt ingredients together\n2. Remove from heat and cool slightly\n3. Pour into mold and cool overnight until solid\n4. Now you have a solid {category.category_name}",
            category_id=category.category_id,
            location_id=location.location_id)
        db.session.add(recipe)
        
        wax = Ingredient.query.get(num) # should be beeswax, rice bran wax, cetyl alcohol
        butter = Ingredient.query.get((num + 3)) # should be shea butter, cocoa butter, mango butter
        oil = Ingredient.query.get((num + 6)) # should be almond oil, jojoba oil, argan oil

        db.session.add(RecipeIngredients(recipe_id=num, ingredient_id=wax.ingredient_id, percentage=33))
        db.session.add(RecipeIngredients(recipe_id=num, ingredient_id=butter.ingredient_id, percentage=33))
        db.session.add(RecipeIngredients(recipe_id=num, ingredient_id=oil.ingredient_id, percentage=33))
        db.session.commit()

