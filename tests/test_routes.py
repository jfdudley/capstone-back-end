import pytest

def test_get_all_recipes_with_one_recipe(client, one_recipe):
    #Act
    response = client.get("/recipes")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body[0]["category"] == "Moisturiser"
    assert response_body[0]["use_location"] == "Body"
    assert response_body[0]["recipe_name"] == "Basic Solid Lotion"
    assert response_body[0]["recipe_description"] == "A basic solid lotion recipe"
    assert response_body[0]["instructions"] == ["1. Melt wax, butter, and oil together", "2. Remove from heat and cool slightly", "3. Pour into mold and cool overnight until solid"]
    assert response_body[0]["ingredient_info"] == [{
                "ingredient_id": 1,
                "ingredient_name": "Beeswax",
                "percentage": 33
            },
            {
                "ingredient_id": 3,
                "ingredient_name": "Shea Butter",
                "percentage": 33
            },
            {
                "ingredient_id": 5,
                "ingredient_name": "Almond Oil",
                "percentage": 33
            }]

