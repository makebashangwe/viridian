global_goal_data = {
  "title": "Earn 10 XP",
  "description": "Build a steady movement habit.",
  "target_type": "total_xp",
  "target_value": 10,
  "reward_points": 5,
  "activity_rule_id": None
}

activity_specific_goal_data = {
  "title": "Complete 3 Walking Sessions",
  "description": "Walk consistently this week.",
  "target_type": "total_sessions",
  "target_value": 3,
  "reward_points": 10,
  "activity_rule_id": 1
}

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
def test_create_new_global_goal(client,auth_header):
    
    goal_response = client.post(
        "/goals",
        headers=auth_header,
        json = global_goal_data
    )

    assert goal_response.status_code ==201
    
    goal_response_data = goal_response.json()
    assert goal_response_data["activity_rule_id"] is None
    assert goal_response_data["progress_value"] == 0
    assert goal_response_data["is_completed"] is False

def test_create_activity_specific_goal (client,auth_header):
    activity_response = client.post(
        "/activities",
        headers = auth_header,
        json = valid_activity_data
    )
    
    assert activity_response.status_code == 201
    
    activity_id = activity_response.json()["id"]

    goal_data = activity_specific_goal_data.copy()

    goal_data["activity_rule_id"] = activity_id
    goal_response = client.post(
        "/goals",
        headers=auth_header,
        json = goal_data
    )

    assert goal_response.status_code ==201

    goal_response_data = goal_response.json()

    assert goal_response_data["activity_rule_id"] == activity_id
    assert goal_response_data["progress_value"] == 0
    assert goal_response_data["target_type"] == "total_sessions"
    assert goal_response_data["target_value"] == 3
    assert goal_response_data["is_completed"] is False
    
def test_get_all_goals(client, auth_header):
    first_response = client.post(
        "/goals",
        headers=auth_header,
        json=global_goal_data
    )

    assert first_response.status_code == 201

    second_goal_data = global_goal_data.copy()
    second_goal_data["title"] = "Complete 2 Sessions"
    second_goal_data["target_type"] = "total_sessions"
    second_goal_data["target_value"] = 2

    second_response = client.post(
        "/goals",
        headers=auth_header,
        json=second_goal_data
    )

    assert second_response.status_code == 201

    response = client.get(
        "/goals",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Earn 10 XP"
    assert data[1]["title"] == "Complete 2 Sessions"

def test_get_goal_by_id(client, auth_header):
    create_response = client.post(
        "/goals",
        headers=auth_header,
        json=global_goal_data
    )

    assert create_response.status_code == 201
    goal_id = create_response.json()["id"]

    response = client.get(
        f"/goals/{goal_id}",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == goal_id
    assert data["title"] == "Earn 10 XP"
    assert data["target_type"] == "total_xp"
    assert data["target_value"] == 10

def test_get_missing_goal(client, auth_header):
    response = client.get(
        "/goals/9999",
        headers=auth_header
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Goal Not Found."

def test_create_goal_with_missing_activity(client, auth_header):
    goal_data = activity_specific_goal_data.copy()
    goal_data["activity_rule_id"] = 9999

    response = client.post(
        "/goals",
        headers=auth_header,
        json=goal_data
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity Rule not Found."

def test_global_xp_goal_progress(client, auth_header):
    goal_response = client.post(
        "/goals",
        headers=auth_header,
        json=global_goal_data
    )

    assert goal_response.status_code == 201
    goal_id = goal_response.json()["id"]

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

    progress_response = client.get(
        f"/goals/{goal_id}/progress",
        headers=auth_header
    )

    assert progress_response.status_code == 200

    data = progress_response.json()

    assert data["goal_id"] == goal_id
    assert data["progress_value"] == 4
    assert data["target_value"] == 10
    assert data["is_completed"] is False
    
def test_global_goal_becomes_completed(client, auth_header):
    goal_data = global_goal_data.copy()
    goal_data["target_value"] = 4

    goal_response = client.post(
        "/goals",
        headers=auth_header,
        json=goal_data
    )

    goal_id = goal_response.json()["id"]

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

    assert session_response.status_code == 201

    progress_response = client.get(
        f"/goals/{goal_id}/progress",
        headers=auth_header
    )

    assert progress_response.status_code == 200

    data = progress_response.json()

    assert data["progress_value"] == 4
    assert data["target_value"] == 4
    assert data["is_completed"] is True

def test_activity_specific_goal_only_counts_matching_activity(
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

    goal_data = activity_specific_goal_data.copy()
    goal_data["activity_rule_id"] = walking_id
    goal_data["target_value"] = 2

    goal_response = client.post(
        "/goals",
        headers=auth_header,
        json=goal_data
    )

    assert goal_response.status_code == 201
    goal_id = goal_response.json()["id"]

    walking_session = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": walking_id,
            "duration_minutes": 30,
            "location": "Neighborhood",
            "notes": None
        }
    )

    yoga_session = client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": yoga_id,
            "duration_minutes": 30,
            "location": "Home",
            "notes": None
        }
    )

    assert walking_session.status_code == 201
    assert yoga_session.status_code == 201

    progress_response = client.get(
        f"/goals/{goal_id}/progress",
        headers=auth_header
    )

    assert progress_response.status_code == 200

    data = progress_response.json()

    assert data["progress_value"] == 1
    assert data["target_value"] == 2
    assert data["is_completed"] is False

def test_get_all_goal_progress(client, auth_header):
    first_goal = client.post(
        "/goals",
        headers=auth_header,
        json=global_goal_data
    )

    second_goal_data = global_goal_data.copy()
    second_goal_data["title"] = "Complete One Session"
    second_goal_data["target_type"] = "total_sessions"
    second_goal_data["target_value"] = 1

    second_goal = client.post(
        "/goals",
        headers=auth_header,
        json=second_goal_data
    )

    assert first_goal.status_code == 201
    assert second_goal.status_code == 201

    activity_response = client.post(
        "/activities",
        headers=auth_header,
        json=valid_activity_data
    )

    activity_id = activity_response.json()["id"]

    client.post(
        "/sessions",
        headers=auth_header,
        json={
            "activity_rule_id": activity_id,
            "duration_minutes": 30,
            "location": "Neighborhood",
            "notes": None
        }
    )

    response = client.get(
        "/goals/progress",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    goals_by_title = {
        goal["title"]: goal
        for goal in data
    }

    assert goals_by_title["Earn 10 XP"]["progress_value"] == 4
    assert goals_by_title["Earn 10 XP"]["is_completed"] is False

    assert goals_by_title["Complete One Session"]["progress_value"] == 1
    assert goals_by_title["Complete One Session"]["is_completed"] is True

def test_goal_rewards_summary(client, auth_header):
    goal_data = global_goal_data.copy()
    goal_data["target_value"] = 4
    goal_data["reward_points"] = 5

    goal_response = client.post(
        "/goals",
        headers=auth_header,
        json=goal_data
    )

    assert goal_response.status_code == 201
    goal_id = goal_response.json()["id"]

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

    assert session_response.status_code == 201

    response = client.get(
        "/goals/rewards-summary",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] > 0
    assert data["completed_goal_count"] == 1
    assert data["reward_points_earned"] == 5
    assert len(data["completed_goals"]) == 1
    assert data["completed_goals"][0]["id"] == goal_id

def test_user_cannot_access_another_users_goal(
    client,
    auth_header
):
    goal_response = client.post(
        "/goals",
        headers=auth_header,
        json=global_goal_data
    )

    assert goal_response.status_code == 201
    goal_id = goal_response.json()["id"]

    register_response = client.post(
        "/auth/register",
        json={
            "email": "secondgoal@example.com",
            "username": "secondgoaluser",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "secondgoal@example.com",
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
        f"/goals/{goal_id}",
        headers=second_user_header
    )

    assert response.status_code == 404

