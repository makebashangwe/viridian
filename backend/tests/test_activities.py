def valid_activity_data():
    return {
        "name": "Walking",
        "difficulty_rank": 1,
        "legal_minutes": 10,
        "legal_points": 1,
        "goal_minutes": 20,
        "goal_points": 2,
        "bonus_interval_minutes": 10,
        "bonus_points": 1,
        "max_session_minutes": 120,
        "default_location": "Neighborhood"
    }

def test_get_activities(client, auth_header):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    assert create_response.status_code == 201

    response = client.get(
        "/activities",
        headers=auth_header
    )

    assert response.status_code == 200

    activities = response.json()

    assert len(activities) == 1
    assert activities[0]["name"] == "Walking"
    assert activities[0]["is_active"] is True

def test_get_activity_by_id(client, auth_header):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    activity_id = create_response.json()["id"]

    response = client.get(
        f"/activities/{activity_id}",
        headers=auth_header
    )

    assert response.status_code == 200

    activity_data = response.json()

    assert activity_data["id"] == activity_id
    assert activity_data["name"] == "Walking"

def test_get_missing_activity(client, auth_header):
    response = client.get(
        "/activities/9999",
        headers=auth_header
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity Rule Not Found."

def test_edit_activity(client, auth_header):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    activity_id = create_response.json()["id"]

    response = client.patch(
        f"/activities/{activity_id}",
        headers=auth_header,
        json={
            "name": "Outdoor Walking",
            "goal_minutes": 30,
            "max_session_minutes": 150
        }
    )

    assert response.status_code == 200

    updated_activity = response.json()

    assert updated_activity["name"] == "Outdoor Walking"
    assert updated_activity["goal_minutes"] == 30
    assert updated_activity["max_session_minutes"] == 150

    # Unchanged fields should remain unchanged.
    assert updated_activity["legal_minutes"] == 10
    assert updated_activity["difficulty_rank"] == 1

def test_activity_creation(client,auth_header):
    activity_rule_creation_response = client.post(
        "/activities",
        headers=auth_header,
        json = {  
            "name": "Walking",
            "difficulty_rank": 1,
            "legal_minutes": 10,
            "legal_points": 1,
            "goal_minutes": 20,
            "goal_points": 2,
            "bonus_interval_minutes": 10,
            "bonus_points": 1,
            "max_session_minutes": 120,
            "default_location": "Neighborhood"
            }
    )
    activity_data = activity_rule_creation_response.json()

    assert activity_rule_creation_response.status_code == 201
    assert activity_data["id"] > 0
    assert activity_data["name"] == "Walking"
    assert activity_data["default_location"] == "Neighborhood"
    assert activity_data["is_active"] is True

def test_invalid_minute_order(client,auth_header):
    activity_rule_creation_response = client.post(
        "/activities",
        headers=auth_header,
        json = {
            "name": "Walking",
            "difficulty_rank": 1,
            "legal_minutes": 30,
            "legal_points": 1,
            "goal_minutes": 20,
            "goal_points": 2,
            "bonus_interval_minutes": 10,
            "bonus_points": 1,
            "max_session_minutes": 120,
            "default_location": "Neighborhood"
        }
    )
    
    assert activity_rule_creation_response.status_code == 422

def test_edit_activity(client, auth_header):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    activity_id = create_response.json()["id"]

    response = client.patch(
        f"/activities/{activity_id}",
        headers=auth_header,
        json={
            "name": "Outdoor Walking",
            "goal_minutes": 30,
            "max_session_minutes": 150
        }
    )

    assert response.status_code == 200

    updated_activity = response.json()

    assert updated_activity["name"] == "Outdoor Walking"
    assert updated_activity["goal_minutes"] == 30
    assert updated_activity["max_session_minutes"] == 150

    # Unchanged fields should remain unchanged.
    assert updated_activity["legal_minutes"] == 10
    assert updated_activity["difficulty_rank"] == 1


def test_edit_activity_with_invalid_merged_minutes(client, auth_header):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    activity_id = create_response.json()["id"]

    response = client.patch(
        f"/activities/{activity_id}",
        headers=auth_header,
        json={
            "legal_minutes": 30
        }
    )

    assert response.status_code == 422
    assert (
        response.json()["detail"]
        == "legal_minutes cannot exceed goal_minutes"
    )

def test_edit_activity_with_goal_above_maximum(client, auth_header):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    activity_id = create_response.json()["id"]

    response = client.patch(
        f"/activities/{activity_id}",
        headers=auth_header,
        json={
            "goal_minutes": 150
        }
    )

    assert response.status_code == 422
    assert (
        response.json()["detail"]
        == "goal_minutes cannot exceed max_session_minutes"
    )
def test_archive_activity(client, auth_header):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    activity_id = create_response.json()["id"]

    archive_response = client.patch(
        f"/activities/{activity_id}/archive",
        headers=auth_header
    )

    assert archive_response.status_code == 200
    assert archive_response.json()["is_active"] is False

def test_archived_activity_is_hidden_from_list(client, auth_header):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    activity_id = create_response.json()["id"]

    archive_response = client.patch(
        f"/activities/{activity_id}/archive",
        headers=auth_header
    )

    assert archive_response.status_code == 200

    list_response = client.get(
        "/activities",
        headers=auth_header
    )

    assert list_response.status_code == 200
    assert list_response.json() == []

def test_archived_activity_is_hidden_by_id(client, auth_header):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    activity_id = create_response.json()["id"]

    client.patch(
        f"/activities/{activity_id}/archive",
        headers=auth_header
    )

    response = client.get(
        f"/activities/{activity_id}",
        headers=auth_header
    )

    assert response.status_code == 404

def test_archived_activity_is_hidden_by_id(client, auth_header):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    activity_id = create_response.json()["id"]

    client.patch(
        f"/activities/{activity_id}/archive",
        headers=auth_header
    )

    response = client.get(
        f"/activities/{activity_id}",
        headers=auth_header
    )

    assert response.status_code == 404

def test_restore_activity(client, auth_header):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    activity_id = create_response.json()["id"]

    archive_response = client.patch(
        f"/activities/{activity_id}/archive",
        headers=auth_header
    )

    assert archive_response.status_code == 200

    restore_response = client.patch(
        f"/activities/{activity_id}/restore",
        headers=auth_header
    )

    assert restore_response.status_code == 200
    assert restore_response.json()["is_active"] is True

    list_response = client.get(
        "/activities",
        headers=auth_header
    )

    assert len(list_response.json()) == 1

def test_user_cannot_access_another_users_activity(
    client,
    auth_header
):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    activity_id = create_response.json()["id"]

    second_register_response = client.post(
        "/auth/register",
        json={
            "email": "second@example.com",
            "username": "seconduser",
            "password": "password123"
        }
    )

    assert second_register_response.status_code == 201

    second_login_response = client.post(
        "/auth/login",
        json={
            "email": "second@example.com",
            "password": "password123"
        }
    )

    assert second_login_response.status_code == 200

    second_token = second_login_response.json()["access_token"]

    second_user_header = {
        "Authorization": f"Bearer {second_token}"
    }

    response = client.get(
        f"/activities/{activity_id}",
        headers=second_user_header
    )

    assert response.status_code == 404

def test_archived_activity_cannot_receive_new_session(
    client,
    auth_header
):
    create_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data()
    )

    activity_id = create_response.json()["id"]

    archive_response = client.patch(
        f"/activities/{activity_id}/archive",
        headers=auth_header
    )

    assert archive_response.status_code == 200

    session_response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 30,
            "location": "Neighborhood",
            "notes": "This should be rejected"
        }
    )

    assert session_response.status_code == 404