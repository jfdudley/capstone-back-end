import pytest

def test_get_all_molds_no_molds_returns_empty_list(client):
    #Act
    response = client.get("/molds")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_molds_with_one_mold(client, one_mold):
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


def test_get_all_molds_with_three_molds(client, three_molds):
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