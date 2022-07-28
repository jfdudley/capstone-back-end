import pytest
from app.models.ingredient import Ingredient


def test_get_all_ingredients_no_info_returns_empty_list(client):
    #Act
    response = client.get("/ingredients")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_ingredients_returns_list(client, nine_ingredients):
    #Act
    response = client.get("/ingredients")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {"ingredient_id" : 1, 
        "ingredient_name" : "Beeswax"},
        {"ingredient_id" : 2, 
        "ingredient_name" : "Rice Bran Wax"},
        {"ingredient_id" : 3, 
        "ingredient_name" : "Cetyl Alcohol"},
        {"ingredient_id" : 4, 
        "ingredient_name" : "Shea Butter"},
        {"ingredient_id" : 5, 
        "ingredient_name" : "Cocoa Butter"},
        {"ingredient_id" : 6, 
        "ingredient_name" : "Mango Butter"},
        {"ingredient_id" : 7, 
        "ingredient_name" : "Almond Oil"},
        {"ingredient_id" : 8, 
        "ingredient_name" : "Jojoba Oil"},
        {"ingredient_id" : 9, 
        "ingredient_name" : "Argan Oil"},]


def test_get_one_ingredient_returns_correct_info_no_recipes(client, nine_ingredients):
    #Act
    response = client.get("/ingredients/4")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {"ingredient_id" : 4, "ingredient_name" : "Shea Butter"}


def test_get_one_ingredient_returns_correct_info_with_recipes(client, three_recipes):
    #Act
    response = client.get("/ingredients/4/recipes")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "ingredient_id" : 4, 
        "ingredient_name" : "Shea Butter", 
        "recipe_info" : [{
            "recipe_id" : 1,
            "recipe_name" : "Basic Solid Moisturizer",
            "percentage" : 33}]
        }


def test_get_one_ingredient_returns_error_with_invalid_info(client, nine_ingredients):
    #Act
    response = client.get("/ingredients/42")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"details" : "Ingredient id: 42 not found."}


def test_patch_one_ingredient_changes_only_that_ingredient_success(client, three_recipes):
    # Arrange
    ingredient_response = client.get("/ingredients/4")
    edited_ingredient_before = ingredient_response.get_json()
    recipe_response = client.get("/recipes/1")
    edited_recipe_before = recipe_response.get_json()

    unchanged_recipe = client.get("/recipes/2")
    unchanged_recipe_before = unchanged_recipe.get_json()
    unchanged_ingredient = client.get("/ingredients/2")
    unchanged_ingredient_before = unchanged_ingredient.get_json()

    new_ingredient_info = { "ingredient_name" : "New Ingredient Name"}

    # Act
    ingredient_patch_response = client.patch("/ingredients/4", json=new_ingredient_info)
    edited_ingredient_after = ingredient_patch_response.get_json()

    edited_recipe_response = client.get("/recipes/1")
    edited_recipe_after = edited_recipe_response.get_json()

    same_recipe_1 = client.get("/recipes/2")
    unchanged_recipe_after = same_recipe_1.get_json()
    same_ingredient_1 = client.get("/ingredients/2")
    unchanged_ingredient_after = same_ingredient_1.get_json()

    # Assert
    assert ingredient_patch_response.status_code == 200
    assert edited_ingredient_before != edited_ingredient_after
    assert edited_recipe_before != edited_recipe_after
    assert edited_ingredient_after["ingredient_name"] == "New Ingredient Name"
    assert edited_recipe_after["ingredient_info"][1]["ingredient_name"] == "New Ingredient Name"
    assert unchanged_ingredient_before == unchanged_ingredient_after
    assert unchanged_recipe_before == unchanged_recipe_after


def test_patch_one_ingredient_recipe_info_returns_error_and_makes_no_changes(client, three_recipes):
    # Arrange
    pre_patch_ingredient_response = client.get("/ingredients/4")
    edited_ingredient_before = pre_patch_ingredient_response.get_json()

    new_ingredient_info = { 
        "ingredient_name" : "New Ingredient Name",
        "recipe_info" : {
            "recipe_id" : 0,
            "recipe_name" : "New Recipe Name",
            "percentage" : 45
        }
        }

    # Act
    ingredient_patch_response = client.patch("/ingredients/4", json=new_ingredient_info)
    patch_response_body = ingredient_patch_response.get_json()

    post_patch_ingredient_response = client.get("/ingredients/4")
    edited_ingredient_after = post_patch_ingredient_response.get_json()

    # Assert
    assert ingredient_patch_response.status_code == 405
    assert patch_response_body == {"details" : "Recipe-ingredient relationships may only be updated from recipe records."}
    assert edited_ingredient_before == edited_ingredient_after


def test_patch_one_ingredient_invalid_info_returns_error_and_makes_no_changes(client, three_recipes):
    # Arrange
    pre_patch_ingredient_response = client.get("/ingredients/4")
    edited_ingredient_before = pre_patch_ingredient_response.get_json()

    new_ingredient_info = { 
        "name" : "New Ingredient Name",
        "info" : "New info here"
        }

    # Act
    ingredient_patch_response = client.patch("/ingredients/4", json=new_ingredient_info)
    patch_response_body = ingredient_patch_response.get_json()

    post_patch_ingredient_response = client.get("/ingredients/4")
    edited_ingredient_after = post_patch_ingredient_response.get_json()

    # Assert
    assert ingredient_patch_response.status_code == 400
    assert patch_response_body == {"details" : "Invalid key(s): ['info', 'name']. Ingredient not updated."}
    assert edited_ingredient_before == edited_ingredient_after


def test_delete_ingredient_no_recipes_deletes_one_ingredient_only(client, nine_ingredients):
    # Arrange
    before_response = client.get("/ingredients")
    ingredient_info_before = before_response.get_json()

    # Act
    delete_response = client.delete("/ingredients/4")
    delete_response_body = delete_response.get_json()

    after_response = client.get("/ingredients")
    ingredient_info_after = after_response.get_json()

    # Assert
    assert delete_response.status_code == 200
    assert delete_response_body == 'Ingredient 4 "Shea Butter" successfully deleted'
    assert len(ingredient_info_before) == 9
    assert len(ingredient_info_after) == 8

    assert Ingredient.query.get(4) is None
    assert Ingredient.query.get(2) is not None
    assert Ingredient.query.get(3) is not None


def test_delete_ingredient_with_recipes_returns_error(client, three_recipes):
    # Arrange
    before_response = client.get("/ingredients/4")
    ingredient_info_before = before_response.get_json()
    recipe_response_before = client.get("/recipes/1")
    recipe_before = recipe_response_before.get_json()

    # Act
    delete_response = client.delete("/ingredients/4")
    delete_response_body = delete_response.get_json()

    after_response = client.get("/ingredients/4")
    ingredient_info_after = after_response.get_json()
    recipe_response_after = client.get("/recipes/1")
    recipe_after = recipe_response_after.get_json()

    # Assert
    assert delete_response.status_code == 405
    assert delete_response_body == {"details" : "Ingredient record is in use and so cannot be deleted."}
    assert recipe_before["ingredient_info"][1]["ingredient_name"] == ingredient_info_before["ingredient_name"]
    assert recipe_after["ingredient_info"][1]["ingredient_name"] == ingredient_info_after["ingredient_name"]
    assert Ingredient.query.get(2) is not None
    