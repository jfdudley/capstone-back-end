import pytest
from app.models.location import Location


def test_get_all_locations_no_info_returns_empty_list(client):
    #Act
    response = client.get("/locations")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_locations_with_info_returns_complete_list(client, three_locations):
    #Act
    response = client.get("/locations")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {"location_id" : 1, 
        "location_name" : "Body"},
        {"location_id" : 2, 
        "location_name" : "Face"},
        {"location_id" : 3, 
        "location_name" : "Lips"}]


def test_get_one_location_returns_correct_info_no_recipes(client, three_locations):
    #Act
    response = client.get("/locations/2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {"location_id" : 2, "location_name" : "Face"}


def test_get_one_location_returns_correct_info_with_recipes(client, three_recipes):
    #Act
    response = client.get("/locations/2/recipes")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "location_id" : 2, 
        "location_name" : "Face", 
        "recipes" : ["Basic Solid Cleanser"]
        }


def test_get_one_location_returns_error_with_invalid_id_num(client, three_locations):
    #Act
    response = client.get("/locations/42")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"details" : "Location id: 42 not found."}


def test_get_one_location_returns_error_with_invalid_id_non_num(client, three_locations):
    #Act
    response = client.get("/locations/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details" : "Invalid id: cat"}


def test_patch_one_location_changes_only_that_location_success(client, three_recipes):
    # Arrange
    location_response = client.get("/locations/2")
    edited_location_before = location_response.get_json()
    recipe_response = client.get("/recipes/2")
    edited_recipe_before = recipe_response.get_json()

    unchanged_recipe = client.get("/recipes/1")
    unchanged_recipe_before = unchanged_recipe.get_json()
    unchanged_location = client.get("/locations/1")
    unchanged_location_before = unchanged_location.get_json()

    new_location_info = { "location_name" : "New Location Name"}

    # Act
    location_patch_response = client.patch("/locations/2", json=new_location_info)
    edited_location_after = location_patch_response.get_json()

    edited_recipe_response = client.get("/recipes/2")
    edited_recipe_after = edited_recipe_response.get_json()

    same_recipe_1 = client.get("/recipes/1")
    unchanged_recipe_after = same_recipe_1.get_json()
    same_location_1 = client.get("/locations/1")
    unchanged_location_after = same_location_1.get_json()

    # Assert
    assert location_patch_response.status_code == 200
    assert edited_location_before != edited_location_after
    assert edited_recipe_before != edited_recipe_after
    assert edited_location_after["location_name"] == "New Location Name"
    assert edited_recipe_after["location"] == "New Location Name"
    assert unchanged_location_before == unchanged_location_after
    assert unchanged_recipe_before == unchanged_recipe_after


def test_patch_one_location_recipe_info_returns_error_and_makes_no_changes(client, three_recipes):
    # Arrange
    pre_patch_location_response = client.get("/locations/2")
    edited_location_before = pre_patch_location_response.get_json()

    new_location_info = { 
        "location_name" : "New Location Name",
        "recipes" : "New Recipe Name"
        }

    # Act
    location_patch_response = client.patch("/locations/2", json=new_location_info)
    patch_response_body = location_patch_response.get_json()

    post_patch_location_response = client.get("/locations/2")
    edited_location_after = post_patch_location_response.get_json()

    # Assert
    assert location_patch_response.status_code == 405
    assert patch_response_body == {"details" : "Recipe-location relationships may only be updated from recipe records."}
    assert edited_location_before == edited_location_after


def test_patch_one_location_invalid_info_returns_error_and_makes_no_changes(client, three_recipes):
    # Arrange
    pre_patch_location_response = client.get("/locations/2")
    edited_location_before = pre_patch_location_response.get_json()

    new_location_info = { 
        "name" : "New Location Name",
        "info" : "New info here"
        }

    # Act
    location_patch_response = client.patch("/locations/2", json=new_location_info)
    patch_response_body = location_patch_response.get_json()

    post_patch_location_response = client.get("/locations/2")
    edited_location_after = post_patch_location_response.get_json()

    # Assert
    assert location_patch_response.status_code == 400
    assert patch_response_body == {"details" : "Invalid key(s): ['info', 'name']. Location not updated."}
    assert edited_location_before == edited_location_after


def test_delete_location_no_recipes_deletes_one_location_only(client, three_locations):
    # Arrange
    before_response = client.get("/locations")
    location_info_before = before_response.get_json()

    # Act
    delete_response = client.delete("/locations/2")
    delete_response_body = delete_response.get_json()

    after_response = client.get("/locations")
    location_info_after = after_response.get_json()

    # Assert
    assert delete_response.status_code == 200
    assert delete_response_body == 'Location 2 "Face" successfully deleted'
    assert len(location_info_before) == 3
    assert len(location_info_after) == 2

    assert Location.query.get(2) is None
    assert Location.query.get(1) is not None
    assert Location.query.get(3) is not None


def test_delete_location_with_recipes_returns_error(client, three_recipes):
    # Arrange
    before_response = client.get("/locations/2")
    location_info_before = before_response.get_json()
    recipe_response_before = client.get("/recipes/2")
    recipe_before = recipe_response_before.get_json()

    # Act
    delete_response = client.delete("/locations/2")
    delete_response_body = delete_response.get_json()

    after_response = client.get("/locations/2")
    location_info_after = after_response.get_json()
    recipe_response_after = client.get("/recipes/2")
    recipe_after = recipe_response_after.get_json()

    # Assert
    assert delete_response.status_code == 405
    assert delete_response_body == {"details" : "Location record is in use and so cannot be deleted."}
    assert recipe_before["location"] == recipe_after["location"]
    assert location_info_before["location_name"] == location_info_after["location_name"]
    assert Location.query.get(2) is not None
    