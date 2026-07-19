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

def test_get_xp_summary(client,auth_header):
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
    
    xp_response = client.get(
        "/xp/summary",
        headers = auth_header
    )

    assert xp_response.status_code == 200
    xp_response_data = xp_response.json()
    assert xp_response_data["user_id"] > 0
    assert xp_response_data["total_points"]  ==4
    assert xp_response_data["total_sessions"] ==1
    assert xp_response_data["legal_goal_completed_total"] == 1
    assert xp_response_data["main_goal_completed_total"] ==1
    assert xp_response_data["bonus_intervals_total"] ==1

def test_get_xp_by_session_id(client,auth_header):
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
    
    session_id = session_response.json()["id"]


    xp_response = client.get(
        f"/xp/by-session/{session_id}",
        headers = auth_header
        )

    assert xp_response.status_code == 200

    xp_response_data = xp_response.json()

    assert xp_response_data["user_id"] > 0
    assert xp_response_data["session_id"]  == session_id
    assert xp_response_data["total_points"] == 4

def test_empty_xp_summary(client, auth_header):
    response = client.get(
        "/xp/summary",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] > 0
    assert data["total_points"] == 0
    assert data["total_sessions"] == 0
    assert data["legal_goal_completed_total"] == 0
    assert data["main_goal_completed_total"] == 0
    assert data["bonus_intervals_total"] == 0

def test_xp_summary_aggregates_multiple_sessions(
    client,
    auth_header
):
    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    assert activity_response.status_code == 201
    activity_id = activity_response.json()["id"]

    first_session_response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 30,
            "location": "Neighborhood",
            "notes": None
        }
    )

    second_session_response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 20,
            "location": "Neighborhood",
            "notes": None
        }
    )

    assert first_session_response.status_code == 201
    assert second_session_response.status_code == 201

    response = client.get(
        "/xp/summary",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    # 30-minute session = 4 points
    # 20-minute session = 3 points
    assert data["total_points"] == 7
    assert data["total_sessions"] == 2
    assert data["legal_goal_completed_total"] == 2
    assert data["main_goal_completed_total"] == 2
    assert data["bonus_intervals_total"] == 1

def test_get_xp_by_activity(client, auth_header):
    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    assert activity_response.status_code == 201
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

    assert session_response.status_code == 201

    response = client.get(
        "/xp/by-activity",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] > 0
    assert data["xp_by_activity"] == {
        "Walking": 4.0
}

def test_get_xp_by_activity_id(client, auth_header):
    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    assert activity_response.status_code == 201
    activity_id = activity_response.json()["id"]

    first_session_response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 30,
            "location": "Neighborhood",
            "notes": None
        }
    )

    second_session_response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 20,
            "location": "Neighborhood",
            "notes": None
        }
    )

    assert first_session_response.status_code == 201
    assert second_session_response.status_code == 201

    response = client.get(
        f"/xp/by-activity/{activity_id}",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] > 0
    assert data["activity_rule_id"] == activity_id
    assert data["total_points"] == 7

def test_get_xp_for_missing_session(client, auth_header):
    response = client.get(
        "/xp/by-session/9999",
        headers=auth_header
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found."

def test_xp_keeps_multiple_activities_separate(
    client,
    auth_header
):
    walking_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    assert walking_response.status_code == 201
    walking_id = walking_response.json()["id"]

    yoga_data = {
        "name": "Yoga",
        "difficulty_rank": 2,
        "legal_minutes": 15,
        "legal_points": 2,
        "goal_minutes": 30,
        "goal_points": 3,
        "bonus_interval_minutes": 15,
        "bonus_points": 1,
        "max_session_minutes": 120,
        "default_location": "Home"
    }

    yoga_response = client.post(
        "/activities",
        headers=auth_header,
        json=yoga_data
    )

    assert yoga_response.status_code == 201
    yoga_id = yoga_response.json()["id"]

    walking_session_response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": walking_id,
            "duration_minutes": 30,
            "location": "Neighborhood",
            "notes": None
        }
    )

    yoga_session_response = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": yoga_id,
            "duration_minutes": 30,
            "location": "Home",
            "notes": None
        }
    )

    assert walking_session_response.status_code == 201
    assert yoga_session_response.status_code == 201

    response = client.get(
        "/xp/by-activity",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] > 0

    xp_by_activity = data["xp_by_activity"]

    assert len(xp_by_activity) == 2
    assert xp_by_activity["Walking"] == 4.0
    assert xp_by_activity["Yoga"] == 5.0

def test_user_cannot_access_another_users_session_xp(
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

    register_response = client.post(
        "/auth/register",
        json={
            "email": "secondxp@example.com",
            "username": "secondxpuser",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "secondxp@example.com",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    second_user_header = {
        "Authorization": (
            f"Bearer {login_response.json()['access_token']}"
        )
    }

    response = client.get(
        f"/xp/by-session/{session_id}",
        headers=second_user_header
    )

    assert response.status_code == 404

