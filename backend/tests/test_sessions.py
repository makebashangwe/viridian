valid_activity_data = {
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


def test_sucessful_session(client,auth_header):
    activity_response = client.post(
        "/activities",
        headers = auth_header,
        json = valid_activity_data
    )

    assert activity_response.status_code == 201
    activity_id = activity_response.json()["id"]

    session_response = client.post(
        "/sessions",
        headers = auth_header,
        json = {
            "activity_rule_id": activity_id,
            "duration_minutes": 30,
            "location": "Neighborhood",
            "notes": "Session test"
            }
        )
    assert session_response.status_code == 201
    session_response_data = session_response.json()

    assert session_response_data["activity_name"] == "Walking"
    assert session_response_data["duration_minutes"] == 30
    assert session_response_data["location"] == "Neighborhood"

    assert session_response_data["points_earned"] == 4
    assert session_response_data["legal_goal_completed"] is True
    assert session_response_data["main_goal_completed"] is True
    assert session_response_data["bonus_intervals"] == 1

def test_session_exceeds_max_duration(client,auth_header):
    activity_response = client.post(
        "/activities",
        headers = auth_header,
        json = valid_activity_data
    )

    assert activity_response.status_code == 201
    activity_id = activity_response.json()["id"]

    session_response = client.post(
        "/sessions",
        headers = auth_header,
        json = {
            "activity_rule_id": activity_id,
            "duration_minutes": 121,
            "location": "Neighborhood",
            "notes": None
            }
        )
    
    assert session_response.status_code == 400
    assert session_response.json()["detail"] == "Session exceeds the maximum allowed duration."

def test_get_sessions(client, auth_header):
    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    activity_id = activity_response.json()["id"]

    create_response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 30,
            "location": "Neighborhood",
            "notes": "List test"
        }
    )

    assert create_response.status_code == 201

    response = client.get(
        "/sessions",
        headers=auth_header
    )

    assert response.status_code == 200

    sessions = response.json()

    assert len(sessions) == 1
    assert sessions[0]["activity_name"] == "Walking"
    assert sessions[0]["points_earned"] == 4

def test_get_session_by_id(client, auth_header):
    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    activity_id = activity_response.json()["id"]

    create_response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 30,
            "location": "Neighborhood",
            "notes": "Get-by-ID test"
        }
    )

    session_id = create_response.json()["id"]

    response = client.get(
        f"/sessions/{session_id}",
        headers=auth_header
    )

    assert response.status_code == 200

    session_data = response.json()

    assert session_data["id"] == session_id
    assert session_data["activity_rule_id"] == activity_id
    assert session_data["notes"] == "Get-by-ID test"

def test_get_missing_session(client, auth_header):
    response = client.get(
        "/sessions/9999",
        headers=auth_header
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found."

def test_delete_session(client, auth_header):
    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    activity_id = activity_response.json()["id"]

    create_response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 30,
            "location": "Neighborhood",
            "notes": None
        }
    )

    session_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/sessions/{session_id}",
        headers=auth_header
    )

    assert delete_response.status_code == 200
    assert (
        delete_response.json()["message"]
        == f"Successfully deleted Session #{session_id}."
    )

    get_response = client.get(
        f"/sessions/{session_id}",
        headers=auth_header
    )

    assert get_response.status_code == 404

def test_create_session_with_missing_activity(client, auth_header):
    response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": 9999,
            "duration_minutes": 30,
            "location": "Neighborhood",
            "notes": None
        }
    )

    assert response.status_code == 404

def test_session_below_legal_goal(client, auth_header):
    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    activity_id = activity_response.json()["id"]

    response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 5,
            "location": "Neighborhood",
            "notes": None
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["points_earned"] == 0
    assert data["legal_goal_completed"] is False
    assert data["main_goal_completed"] is False
    assert data["bonus_intervals"] == 0

def test_session_exactly_at_legal_goal(client, auth_header):
    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    activity_id = activity_response.json()["id"]

    response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 10,
            "location": "Neighborhood",
            "notes": None
        }
    )

    data = response.json()

    assert response.status_code == 201
    assert data["points_earned"] == 1
    assert data["legal_goal_completed"] is True
    assert data["main_goal_completed"] is False
    assert data["bonus_intervals"] == 0

def test_session_exactly_at_main_goal(client, auth_header):
    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    activity_id = activity_response.json()["id"]

    response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 20,
            "location": "Neighborhood",
            "notes": None
        }
    )

    data = response.json()

    assert response.status_code == 201
    assert data["points_earned"] == 3
    assert data["legal_goal_completed"] is True
    assert data["main_goal_completed"] is True
    assert data["bonus_intervals"] == 0


def test_session_multiple_bonus_intervals(client, auth_header):
    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    activity_id = activity_response.json()["id"]

    response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 50,
            "location": "Neighborhood",
            "notes": None
        }
    )

    data = response.json()

    assert response.status_code == 201
    assert data["points_earned"] == 6
    assert data["legal_goal_completed"] is True
    assert data["main_goal_completed"] is True
    assert data["bonus_intervals"] == 3

def test_archived_activity_cannot_create_session(
    client,
    auth_header
):
    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    activity_id = activity_response.json()["id"]

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
            "notes": None
        }
    )

    assert session_response.status_code == 404

def test_user_cannot_access_another_users_session(
    client,
    auth_header
):
    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    activity_id = activity_response.json()["id"]

    session_response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 30,
            "location": "Neighborhood",
            "notes": None
        }
    )

    session_id = session_response.json()["id"]

    second_register_response = client.post(
        "/auth/register",
        json={
            "email": "secondsession@example.com",
            "username": "secondsessionuser",
            "password": "password123"
        }
    )

    assert second_register_response.status_code == 201

    second_login_response = client.post(
        "/auth/login",
        json={
            "email": "secondsession@example.com",
            "password": "password123"
        }
    )

    second_token = second_login_response.json()["access_token"]

    second_user_header = {
        "Authorization": f"Bearer {second_token}"
    }

    response = client.get(
        f"/sessions/{session_id}",
        headers=second_user_header
    )

    assert response.status_code == 404