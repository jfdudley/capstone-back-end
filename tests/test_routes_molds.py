import pytest
from app.models.mold import Mold


def test_get_all_molds_no_info_returns_empty_list(client):
    #Act
    response = client.get("/molds")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_molds_with_one_mold_returns_success(client, one_mold):
    #Act
    response = client.get("/molds")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body[0]["mold_id"] == 1
    assert response_body[0]["well_shape"] == "Flower"
    assert response_body[0]["well_volume_grams"] == 30
    assert response_body[0]["num_wells"] == 12
    assert response_body[0]["source"] == "Brambleberry"


def test_get_all_molds_with_three_molds_returns_success(client, three_molds):
    #Act
    response = client.get("/molds")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    # mold 1
    assert response_body[0]["mold_id"] == 1
    assert response_body[0]["well_shape"] == "Circle"
    assert response_body[0]["well_volume_grams"] == 30
    assert response_body[0]["num_wells"] == 4
    assert response_body[0]["source"] == "Etsy"
    # mold 2
    assert response_body[1]["mold_id"] == 2
    assert response_body[1]["well_shape"] == "Rectangle"
    assert response_body[1]["well_volume_grams"] == 100
    assert response_body[1]["num_wells"] == 10
    assert response_body[1]["source"] == "Brambleberry"
    # mold 3
    assert response_body[2]["mold_id"] == 3
    assert response_body[2]["well_shape"] == "Oval"
    assert response_body[2]["well_volume_grams"] == 75
    assert response_body[2]["num_wells"] == 12
    assert response_body[2]["source"] == "Side of the road"


def test_create_new_mold_returns_success(client, three_molds):
    # Arrange
    new_mold = {
        "well_shape" : "Star",
        "well_volume_grams" : 42,
        "num_wells" : 4,
        "source" : "My imagination"
    }

    all_molds_call_before = client.get("/molds")
    all_molds_before = all_molds_call_before.get_json()

    # Act
    response = client.post("/molds", json=new_mold)
    response_body = response.get_json()

    all_molds_call_after = client.get("/molds")
    all_molds_after = all_molds_call_after.get_json()

    # Assert
    assert response.status_code == 201
    assert len(all_molds_before) == 3
    assert len(all_molds_after) == 4
    assert response_body["mold_id"] == 4
    assert response_body["well_shape"] == "Star"
    assert response_body["well_volume_grams"] == 42
    assert response_body["num_wells"] == 4
    assert response_body["source"] == "My imagination"


def test_get_one_mold_returns_correct_info(client, three_molds):
    #Act
    response = client.get("/molds/2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["mold_id"] == 2
    assert response_body["well_shape"] == "Rectangle"
    assert response_body["well_volume_grams"] == 100
    assert response_body["num_wells"] == 10
    assert response_body["source"] == "Brambleberry"


def test_get_one_mold_returns_error_with_invalid_id_num(client, three_molds):
    #Act
    response = client.get("/molds/42")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"details" : "Mold id: 42 not found."}


def test_get_one_mold_returns_error_with_invalid_id_non_num(client, three_molds):
    #Act
    response = client.get("/molds/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details" : "Invalid id: cat"}


def test_patch_one_mold_changes_only_that_mold_success(client, three_molds):
    # Arrange
    mold_response = client.get("/molds/2")
    edited_mold_before = mold_response.get_json()

    unchanged_mold = client.get("/molds/1")
    unchanged_mold_before = unchanged_mold.get_json()

    new_mold_info = { "well_shape" : "New Mold Shape"}

    # Act
    mold_patch_response = client.patch("/molds/2", json=new_mold_info)
    edited_mold_after = mold_patch_response.get_json()

    same_mold_1 = client.get("/molds/1")
    unchanged_mold_after = same_mold_1.get_json()

    # Assert
    assert mold_patch_response.status_code == 200
    assert edited_mold_before != edited_mold_after
    assert edited_mold_after["well_shape"] == "New Mold Shape"
    assert unchanged_mold_before == unchanged_mold_after


def test_patch_one_mold_invalid_info_returns_error_and_makes_no_changes(client, three_molds):
    # Arrange
    pre_patch_mold_response = client.get("/molds/2")
    edited_mold_before = pre_patch_mold_response.get_json()

    new_mold_info = { 
        "name" : "New Mold Name",
        "info" : "New info here"
        }

    # Act
    mold_patch_response = client.patch("/molds/2", json=new_mold_info)
    patch_response_body = mold_patch_response.get_json()

    post_patch_mold_response = client.get("/molds/2")
    edited_mold_after = post_patch_mold_response.get_json()

    # Assert
    assert mold_patch_response.status_code == 400
    assert patch_response_body == {"details" : "Invalid key(s): ['info', 'name']. Mold not updated."}
    assert edited_mold_before == edited_mold_after


def test_delete_mold_deletes_one_mold_only(client, three_molds):
    # Arrange
    before_response = client.get("/molds")
    mold_info_before = before_response.get_json()

    # Act
    delete_response = client.delete("/molds/2")
    delete_response_body = delete_response.get_json()

    after_response = client.get("/molds")
    mold_info_after = after_response.get_json()

    # Assert
    assert delete_response.status_code == 200
    assert delete_response_body == 'Mold 2 "Rectangle" successfully deleted'
    assert len(mold_info_before) == 3
    assert len(mold_info_after) == 2

    assert Mold.query.get(2) is None
    assert Mold.query.get(1) is not None
    assert Mold.query.get(3) is not None
