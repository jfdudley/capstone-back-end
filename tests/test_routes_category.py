import pytest
from app.models.category import Category

def test_get_all_categories_no_info_returns_empty_list(client):
    #Act
    response = client.get("/categories")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_categories_returns_list(client, three_categories):
    #Act
    response = client.get("/categories")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {"category_id" : 1, 
        "category_name" : "Moisturizer"},
        {"category_id" : 2, 
        "category_name" : "Cleanser"},
        {"category_id" : 3, 
        "category_name" : "Scrub"}]


def test_get_one_category_returns_correct_info_no_recipes(client, three_categories):
    #Act
    response = client.get("/categories/2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {"category_id" : 2, "category_name" : "Cleanser"}


def test_get_one_category_returns_correct_info_with_recipes(client, three_recipes):
    #Act
    response = client.get("/categories/2/recipes")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "category_id" : 2, 
        "category_name" : "Cleanser", 
        "recipes" : ["Basic Solid Cleanser"]
        }


def test_get_one_category_returns_error_with_invalid_info(client, three_categories):
    #Act
    response = client.get("/categories/42")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"details" : "Category id: 42 not found."}


def test_patch_one_category_changes_only_that_category_success(client, three_recipes):
    # Arrange
    category_response = client.get("/categories/2")
    edited_category_before = category_response.get_json()
    recipe_response = client.get("/recipes/2")
    edited_recipe_before = recipe_response.get_json()

    unchanged_recipe = client.get("/recipes/1")
    unchanged_recipe_before = unchanged_recipe.get_json()
    unchanged_category = client.get("/categories/1")
    unchanged_category_before = unchanged_category.get_json()

    new_category_info = { "category_name" : "New Category Name"}

    # Act
    category_patch_response = client.patch("/categories/2", json=new_category_info)
    edited_category_after = category_patch_response.get_json()

    edited_recipe_response = client.get("/recipes/2")
    edited_recipe_after = edited_recipe_response.get_json()

    same_recipe_1 = client.get("/recipes/1")
    unchanged_recipe_after = same_recipe_1.get_json()
    same_category_1 = client.get("/categories/1")
    unchanged_category_after = same_category_1.get_json()

    # Assert
    assert category_patch_response.status_code == 200
    assert edited_category_before != edited_category_after
    assert edited_recipe_before != edited_recipe_after
    assert edited_category_after["category_name"] == "New Category Name"
    assert edited_recipe_after["category"] == "New Category Name"
    assert unchanged_category_before == unchanged_category_after
    assert unchanged_recipe_before == unchanged_recipe_after


def test_patch_one_category_recipe_info_returns_error_and_makes_no_changes(client, three_recipes):
    # Arrange
    pre_patch_category_response = client.get("/categories/2")
    edited_category_before = pre_patch_category_response.get_json()

    new_category_info = { 
        "category_name" : "New Category Name",
        "recipes" : "New Recipe Name"
        }

    # Act
    category_patch_response = client.patch("/categories/2", json=new_category_info)
    patch_response_body = category_patch_response.get_json()

    post_patch_category_response = client.get("/categories/2")
    edited_category_after = post_patch_category_response.get_json()

    # Assert
    assert category_patch_response.status_code == 405
    assert patch_response_body == {"details" : "Recipe-category relationships may only be updated from recipe records."}
    assert edited_category_before == edited_category_after


def test_patch_one_category_invalid_info_returns_error_and_makes_no_changes(client, three_recipes):
    # Arrange
    pre_patch_category_response = client.get("/categories/2")
    edited_category_before = pre_patch_category_response.get_json()

    new_category_info = { 
        "name" : "New Category Name",
        "info" : "New info here"
        }

    # Act
    category_patch_response = client.patch("/categories/2", json=new_category_info)
    patch_response_body = category_patch_response.get_json()

    post_patch_category_response = client.get("/categories/2")
    edited_category_after = post_patch_category_response.get_json()

    # Assert
    assert category_patch_response.status_code == 400
    assert patch_response_body == {"details" : "Invalid key(s): ['info', 'name']. Category not updated."}
    assert edited_category_before == edited_category_after


def test_delete_category_no_recipes_deletes_one_category_only(client, three_categories):
    # Arrange
    before_response = client.get("/categories")
    category_info_before = before_response.get_json()

    # Act
    delete_response = client.delete("/categories/2")
    delete_response_body = delete_response.get_json()

    after_response = client.get("/categories")
    category_info_after = after_response.get_json()

    # Assert
    assert delete_response.status_code == 200
    assert delete_response_body == 'Category 2 "Cleanser" successfully deleted'
    assert len(category_info_before) == 3
    assert len(category_info_after) == 2

    assert Category.query.get(2) is None
    assert Category.query.get(1) is not None
    assert Category.query.get(3) is not None


def test_delete_category_with_recipes_returns_error(client, three_recipes):
    # Arrange
    before_response = client.get("/categories/2")
    category_info_before = before_response.get_json()
    recipe_response_before = client.get("/recipes/2")
    recipe_before = recipe_response_before.get_json()

    # Act
    delete_response = client.delete("/categories/2")
    delete_response_body = delete_response.get_json()

    after_response = client.get("/categories/2")
    category_info_after = after_response.get_json()
    recipe_response_after = client.get("/recipes/2")
    recipe_after = recipe_response_after.get_json()

    # Assert
    assert delete_response.status_code == 405
    assert delete_response_body == {"details" : "Category record is in use and so cannot be deleted."}
    assert recipe_before["category"] == category_info_before["category_name"]
    assert recipe_after["category"] == category_info_after["category_name"]
    assert Category.query.get(2) is not None
    