import pytest
from app.models.recipe import Recipe

def test_get_all_recipies_no_recipe_returns_empty_list(client):
    #Act
    response = client.get("/recipes")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_recipes_with_one_recipe(client, one_recipe):
    #Act
    response = client.get("/recipes")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body[0]["category"] == "Moisturizer"
    assert response_body[0]["location"] == "Body"
    assert response_body[0]["recipe_name"] == "Basic Solid Lotion"
    assert response_body[0]["recipe_description"] == "A basic solid lotion recipe"
    assert response_body[0]["instructions"] == ["1. Melt wax, butter, and oil together", "2. Remove from heat and cool slightly", "3. Pour into mold and cool overnight until solid"]
    assert response_body[0]["ingredient_info"] == [{
                "ingredient_id": 1,
                "ingredient_name": "Beeswax",
                "percentage": 33
            },
            {
                "ingredient_id": 4,
                "ingredient_name": "Shea Butter",
                "percentage": 33
            },
            {
                "ingredient_id": 7,
                "ingredient_name": "Almond Oil",
                "percentage": 33
            }]


def test_get_all_recipes_with_three_recipe(client, three_recipes):
    #Act
    response = client.get("/recipes")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200

    # recipe 1
    assert response_body[0]["category"] == "Moisturizer"
    assert response_body[0]["location"] == "Body"
    assert response_body[0]["recipe_name"] == "Basic Solid Moisturizer"
    assert response_body[0]["recipe_description"] == "A basic solid Moisturizer recipe"
    assert response_body[0]["instructions"] == [
        "1. Melt ingredients together", 
        "2. Remove from heat and cool slightly", 
        "3. Pour into mold and cool overnight until solid", 
        "4. Now you have a solid Moisturizer"
        ]
    assert response_body[0]["ingredient_info"] == [{
                "ingredient_id": 1,
                "ingredient_name": "Beeswax",
                "percentage": 33
            },
            {
                "ingredient_id": 4,
                "ingredient_name": "Shea Butter",
                "percentage": 33
            },
            {
                "ingredient_id": 7,
                "ingredient_name": "Almond Oil",
                "percentage": 33
            }]
    # recipe 2
    assert response_body[1]["category"] == "Cleanser"
    assert response_body[1]["location"] == "Face"
    assert response_body[1]["recipe_name"] == "Basic Solid Cleanser"
    assert response_body[1]["recipe_description"] == "A basic solid Cleanser recipe"
    assert response_body[1]["instructions"] == [
        "1. Melt ingredients together", 
        "2. Remove from heat and cool slightly", 
        "3. Pour into mold and cool overnight until solid", 
        "4. Now you have a solid Cleanser"]
    assert response_body[1]["ingredient_info"] == [{
                "ingredient_id": 2,
                "ingredient_name": "Rice Bran Wax",
                "percentage": 33
            },
            {
                "ingredient_id": 5,
                "ingredient_name": "Cocoa Butter",
                "percentage": 33
            },
            {
                "ingredient_id": 8,
                "ingredient_name": "Jojoba Oil",
                "percentage": 33
            }]
    # recipe 3
    assert response_body[2]["category"] == "Scrub"
    assert response_body[2]["location"] == "Lips"
    assert response_body[2]["recipe_name"] == "Basic Solid Scrub"
    assert response_body[2]["recipe_description"] == "A basic solid Scrub recipe"
    assert response_body[2]["instructions"] == [
        "1. Melt ingredients together", 
        "2. Remove from heat and cool slightly", 
        "3. Pour into mold and cool overnight until solid", 
        "4. Now you have a solid Scrub"]
    assert response_body[2]["ingredient_info"] == [{
                "ingredient_id": 3,
                "ingredient_name": "Cetyl Alcohol",
                "percentage": 33
            },
            {
                "ingredient_id": 6,
                "ingredient_name": "Mango Butter",
                "percentage": 33
            },
            {
                "ingredient_id": 9,
                "ingredient_name": "Argan Oil",
                "percentage": 33
            }]


def test_get_one_recipe_by_id_returns_correct_recipe(client, three_recipes):
    # Act
    response = client.get("/recipes/2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["recipe_id"] == 2
    assert response_body["category"] == "Cleanser"
    assert response_body["location"] == "Face"
    assert response_body["recipe_name"] == "Basic Solid Cleanser"
    assert response_body["recipe_description"] == "A basic solid Cleanser recipe"
    assert response_body["instructions"] == [
        "1. Melt ingredients together", 
        "2. Remove from heat and cool slightly", 
        "3. Pour into mold and cool overnight until solid", 
        "4. Now you have a solid Cleanser"]
    assert response_body["ingredient_info"] == [{
                "ingredient_id": 2,
                "ingredient_name": "Rice Bran Wax",
                "percentage": 33
            },
            {
                "ingredient_id": 5,
                "ingredient_name": "Cocoa Butter",
                "percentage": 33
            },
            {
                "ingredient_id": 8,
                "ingredient_name": "Jojoba Oil",
                "percentage": 33
            }]


def test_get_one_recipe_invalid_id_returns_error(client, three_recipes):
    #Act
    response = client.get("/recipes/20")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"details" : "Recipe id: 20 not found."}

def test_add_new_recipe_existing_data_only_success(client, one_recipe):
    # Arrange
    new_recipe = {
            "recipe_name" : "New Solid Lotion",
            "recipe_description" : "Another lotion recipe",
            "category" : "Moisturizer",
            "location" : "Body",
            "ingredient_info": {
                "Beeswax" : 33,
                "Shea Butter" : 33,
                "Almond Oil" : 33,
            },
            "recipe_instructions" : "1. Instructions go here\n2. Some more down here"
    }

    # Act
    response = client.post("/recipes", json=new_recipe)
    response_body = response.get_json()
    all_recipes = client.get("/recipes")
    all_recipes_response = all_recipes.get_json()
    ###
    # Do get all requests to category, location, and ingredient routes


    # Assert
    assert response.status_code == 201
    assert len(all_recipes_response) == 2
    assert response_body["category"] == "Moisturizer"
    assert response_body["location"] == "Body"
    assert response_body["recipe_name"] == "New Solid Lotion"
    assert response_body["recipe_description"] == "Another lotion recipe"
    assert response_body["instructions"] == ["1. Instructions go here", "2. Some more down here"]
    assert all_recipes_response[0] != all_recipes_response[1]
    assert all_recipes_response[0]["category"] == all_recipes_response[1]["category"]
    assert all_recipes_response[0]["location"] == all_recipes_response[1]["location"]
    assert sorted(all_recipes_response[0]["ingredient_info"], key=lambda x: x["ingredient_name"]) == sorted(all_recipes_response[1]["ingredient_info"], key=lambda x: x["ingredient_name"])
    assert all_recipes_response[0]["recipe_name"] != all_recipes_response[1]["recipe_name"]
    assert all_recipes_response[0]["recipe_description"] != all_recipes_response[1]["recipe_description"]
    assert all_recipes_response[0]["instructions"] != all_recipes_response[1]["instructions"]
    ###
    # check that length of responses for get all category, location, and ingredient routes are still 1, 1, and 3


def test_add_new_recipe_existing_data_only_success(client, one_recipe):
    # Arrange
    new_recipe = {
            "recipe_name" : "New Solid Lotion",
            "recipe_description" : "Another lotion recipe",
            "category" : "New Category",
            "location" : "New Location",
            "ingredient_info": {
                "New wax" : 33,
                "New Butter" : 33,
                "New Oil" : 33
            },
            "recipe_instructions" : "1. Instructions go here\n2. Some more down here"
    }

    # Act
    response = client.post("/recipes", json=new_recipe)
    response_body = response.get_json()
    all_recipes = client.get("/recipes")
    all_recipes_response = all_recipes.get_json()
    ###
    # Do get all requests to category, location, and ingredient routes

    # Assert
    assert response.status_code == 201
    assert len(all_recipes_response) == 2
    assert response_body["category"] == "New Category"
    assert response_body["location"] == "New Location"
    assert response_body["recipe_name"] == "New Solid Lotion"
    assert response_body["recipe_description"] == "Another lotion recipe"
    assert response_body["instructions"] == ["1. Instructions go here", "2. Some more down here"]
    assert all_recipes_response[0] != all_recipes_response[1]
    assert all_recipes_response[0]["category"] != all_recipes_response[1]["category"]
    assert all_recipes_response[0]["location"] != all_recipes_response[1]["location"]
    assert all_recipes_response[0]["recipe_name"] != all_recipes_response[1]["recipe_name"]
    assert all_recipes_response[0]["recipe_description"] != all_recipes_response[1]["recipe_description"]
    assert all_recipes_response[0]["instructions"] != all_recipes_response[1]["instructions"]
    ###
    # check that length of responses for get all category, location, and ingredient routes have increased


def test_patch_one_recipe_by_id_returns_updated_recipe(client, three_recipes):
    # Arrange
    response = client.get("/recipes/2")
    edited_recipe_before = response.get_json()

    unchanged_recipe = client.get("/recipes/1")
    unchanged_recipe_before = unchanged_recipe.get_json()

    new_recipe_info = {
            "recipe_name" : "New Lotion Name",
            "recipe_description" : "New Lotion Description",
            "category" : "New Category",
            "location" : "New Location",
            "ingredient_info": {
                "New wax" : 33,
                "New Butter" : 33,
                "New Oil" : 33,
                "Rice Bran Wax" : 0,
                "Cocoa Butter" : 0,
                "Jojoba Oil" : 0,
            },
            "recipe_instructions" : "1. Instructions go here\n2. Some more down here"
    }

    # Act
    patch_response = client.patch("/recipes/2", json=new_recipe_info)
    edited_recipe_after = patch_response.get_json()

    unchanged_recipe = client.get("/recipes/1")
    unchanged_recipe_after = unchanged_recipe.get_json()

    # Assert
    assert response.status_code == 200
    assert edited_recipe_before["recipe_id"] == 2
    assert edited_recipe_before["category"] != edited_recipe_after["category"]
    assert edited_recipe_before["location"] != edited_recipe_after["location"]
    assert edited_recipe_before["recipe_name"] != edited_recipe_after["recipe_name"]
    assert edited_recipe_before["recipe_description"] != edited_recipe_after["recipe_description"]
    assert edited_recipe_before["instructions"] != edited_recipe_after["instructions"]
    assert edited_recipe_before["ingredient_info"] != edited_recipe_after["ingredient_info"]

    assert edited_recipe_after["recipe_id"] == 2
    assert edited_recipe_after["category"] == "New Category"
    assert edited_recipe_after["location"] == "New Location"
    assert edited_recipe_after["recipe_name"] == "New Lotion Name"
    assert edited_recipe_after["recipe_description"] == "New Lotion Description"
    assert edited_recipe_after["instructions"] == ["1. Instructions go here", "2. Some more down here"]

    assert unchanged_recipe_before == unchanged_recipe_after
    ###
    # check that length of responses for get all category, location, and ingredient routes have increased
    # find a way to test that deleted ingredients are no longer in ingredients list


def test_delete_recipe_deletes_one_recipe(client, three_recipes):
    # Arrange
    before_response = client.get("/recipes")
    recipe_info_before = before_response.get_json()

    # Act
    delete_response = client.delete("/recipes/2")
    delete_response_body = delete_response.get_json()

    after_response = client.get("/recipes")
    recipe_info_after = after_response.get_json()

    # Assert
    assert delete_response.status_code == 200
    assert delete_response_body == 'Recipe 2 "Basic Solid Cleanser" successfully deleted'
    assert len(recipe_info_before) == 3
    assert len(recipe_info_after) == 2

    assert Recipe.query.get(2) is None
    assert Recipe.query.get(1) is not None
    assert Recipe.query.get(3) is not None