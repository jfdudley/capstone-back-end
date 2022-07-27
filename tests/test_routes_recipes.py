import pytest

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