normal_reward_data = {
    "name": "Movie Night",
    "description": "Enjoy a movie after steady progress.",
    "tag": "entertainment",
    "point_cost": 5,
    "estimated_cost": 20,
    "image_url": None,
    "is_locked": False,
    "required_goal_id": None
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

goal_data = {
    "title": "Complete One Session",
    "description": "Complete one activity session.",
    "target_type": "total_sessions",
    "target_value": 1,
    "reward_points": 10,
    "activity_rule_id": None
}


def create_completed_goal(client, auth_header):
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
    assert progress_response.json()["is_completed"] is True

    return goal_id


def test_create_normal_reward(client, auth_header):
    response = client.post(
        "/rewards",
        headers=auth_header,
        json=normal_reward_data
    )

    assert response.status_code == 201

    data = response.json()

    assert data["user_id"] > 0
    assert data["name"] == "Movie Night"
    assert data["description"] == (
        "Enjoy a movie after steady progress."
    )
    assert data["tag"] == "entertainment"
    assert data["point_cost"] == 5
    assert data["estimated_cost"] == 20
    assert data["image_url"] is None
    assert data["is_locked"] is False
    assert data["required_goal_id"] is None


def test_get_all_rewards(client, auth_header):
    first_response = client.post(
        "/rewards",
        headers=auth_header,
        json=normal_reward_data
    )

    assert first_response.status_code == 201

    second_reward_data = normal_reward_data.copy()
    second_reward_data["name"] = "Fancy Coffee"
    second_reward_data["description"] = "Get a favorite coffee."
    second_reward_data["tag"] = "food"
    second_reward_data["point_cost"] = 3

    second_response = client.post(
        "/rewards",
        headers=auth_header,
        json=second_reward_data
    )

    assert second_response.status_code == 201

    response = client.get(
        "/rewards",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    reward_names = {
        reward["name"]
        for reward in data
    }

    assert reward_names == {
        "Movie Night",
        "Fancy Coffee"
    }


def test_get_reward_by_id(client, auth_header):
    create_response = client.post(
        "/rewards",
        headers=auth_header,
        json=normal_reward_data
    )

    assert create_response.status_code == 201
    reward_id = create_response.json()["id"]

    response = client.get(
        f"/rewards/{reward_id}",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == reward_id
    assert data["name"] == "Movie Night"
    assert data["point_cost"] == 5


def test_get_missing_reward(client, auth_header):
    response = client.get(
        "/rewards/9999",
        headers=auth_header
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Reward Not Found."


def test_empty_reward_balance(client, auth_header):
    response = client.get(
        "/rewards/balance",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] > 0
    assert data["reward_points_earned"] == 0
    assert data["reward_points_spent"] == 0
    assert data["available_balance"] == 0


def test_reward_balance_includes_completed_goal(
    client,
    auth_header
):
    create_completed_goal(client, auth_header)

    response = client.get(
        "/rewards/balance",
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()

    assert data["reward_points_earned"] == 10
    assert data["reward_points_spent"] == 0
    assert data["available_balance"] == 10


def test_redeem_reward_successfully(client, auth_header):
    create_completed_goal(client, auth_header)

    reward_response = client.post(
        "/rewards",
        headers=auth_header,
        json=normal_reward_data
    )

    assert reward_response.status_code == 201
    reward_id = reward_response.json()["id"]

    redemption_response = client.post(
        f"/rewards/{reward_id}/redeem",
        headers=auth_header
    )

    assert redemption_response.status_code == 201

    data = redemption_response.json()

    assert data["user_id"] > 0
    assert data["reward_id"] == reward_id
    assert data["reward_name"] == "Movie Night"
    assert data["point_cost"] == 5
    assert data["redeemed_at"] is not None

    balance_response = client.get(
        "/rewards/balance",
        headers=auth_header
    )

    assert balance_response.status_code == 200

    balance = balance_response.json()

    assert balance["reward_points_earned"] == 10
    assert balance["reward_points_spent"] == 5
    assert balance["available_balance"] == 5


def test_cannot_redeem_reward_without_enough_points(
    client,
    auth_header
):
    reward_response = client.post(
        "/rewards",
        headers=auth_header,
        json=normal_reward_data
    )

    assert reward_response.status_code == 201
    reward_id = reward_response.json()["id"]

    response = client.post(
        f"/rewards/{reward_id}/redeem",
        headers=auth_header
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Not Enough Points."


def test_create_locked_reward_with_goal(
    client,
    auth_header
):
    goal_response = client.post(
        "/goals",
        headers=auth_header,
        json=goal_data
    )

    assert goal_response.status_code == 201
    goal_id = goal_response.json()["id"]

    locked_reward_data = normal_reward_data.copy()
    locked_reward_data["name"] = "New Game"
    locked_reward_data["is_locked"] = True
    locked_reward_data["required_goal_id"] = goal_id

    response = client.post(
        "/rewards",
        headers=auth_header,
        json=locked_reward_data
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "New Game"
    assert data["is_locked"] is True
    assert data["required_goal_id"] == goal_id


def test_locked_reward_without_goal_is_rejected(
    client,
    auth_header
):
    locked_reward_data = normal_reward_data.copy()
    locked_reward_data["is_locked"] = True
    locked_reward_data["required_goal_id"] = None

    response = client.post(
        "/rewards",
        headers=auth_header,
        json=locked_reward_data
    )

    # Pydantic rejects this before the route runs.
    assert response.status_code == 422


def test_create_reward_with_missing_goal(
    client,
    auth_header
):
    reward_data = normal_reward_data.copy()
    reward_data["is_locked"] = True
    reward_data["required_goal_id"] = 9999

    response = client.post(
        "/rewards",
        headers=auth_header,
        json=reward_data
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Goal not Found."


def test_cannot_redeem_locked_reward_with_incomplete_goal(
    client,
    auth_header
):
    incomplete_goal_data = goal_data.copy()
    incomplete_goal_data["target_value"] = 2

    goal_response = client.post(
        "/goals",
        headers=auth_header,
        json=incomplete_goal_data
    )

    assert goal_response.status_code == 201
    goal_id = goal_response.json()["id"]

    locked_reward_data = normal_reward_data.copy()
    locked_reward_data["name"] = "Locked Movie Night"
    locked_reward_data["is_locked"] = True
    locked_reward_data["required_goal_id"] = goal_id

    reward_response = client.post(
        "/rewards",
        headers=auth_header,
        json=locked_reward_data
    )

    assert reward_response.status_code == 201
    reward_id = reward_response.json()["id"]

    response = client.post(
        f"/rewards/{reward_id}/redeem",
        headers=auth_header
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Required goal is not completed."
    )


def test_redeem_locked_reward_after_goal_completion(
    client,
    auth_header
):
    goal_id = create_completed_goal(
        client,
        auth_header
    )

    locked_reward_data = normal_reward_data.copy()
    locked_reward_data["name"] = "Unlocked Movie Night"
    locked_reward_data["is_locked"] = True
    locked_reward_data["required_goal_id"] = goal_id

    reward_response = client.post(
        "/rewards",
        headers=auth_header,
        json=locked_reward_data
    )

    assert reward_response.status_code == 201
    reward_id = reward_response.json()["id"]

    response = client.post(
        f"/rewards/{reward_id}/redeem",
        headers=auth_header
    )

    assert response.status_code == 201

    data = response.json()

    assert data["reward_id"] == reward_id
    assert data["reward_name"] == "Unlocked Movie Night"
    assert data["point_cost"] == 5


def test_archive_reward(client, auth_header):
    create_response = client.post(
        "/rewards",
        headers=auth_header,
        json=normal_reward_data
    )

    assert create_response.status_code == 201
    reward_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/rewards/{reward_id}",
        headers=auth_header
    )

    assert delete_response.status_code == 200

    data = delete_response.json()

    assert data["message"] == (
        f"Reward #{reward_id} archived and removed."
    )
    assert data["archive_id"] > 0

    get_response = client.get(
        f"/rewards/{reward_id}",
        headers=auth_header
    )

    assert get_response.status_code == 404


def test_archive_missing_reward(client, auth_header):
    response = client.delete(
        "/rewards/9999",
        headers=auth_header
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Reward Not Found."


def test_user_cannot_access_another_users_reward(
    client,
    auth_header
):
    create_response = client.post(
        "/rewards",
        headers=auth_header,
        json=normal_reward_data
    )

    assert create_response.status_code == 201
    reward_id = create_response.json()["id"]

    register_response = client.post(
        "/auth/register",
        json={
            "email": "secondreward@example.com",
            "username": "secondrewarduser",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "secondreward@example.com",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    second_user_header = {
        "Authorization": (
            f"Bearer {login_response.json()['access_token']}"
        )
    }

    get_response = client.get(
        f"/rewards/{reward_id}",
        headers=second_user_header
    )

    assert get_response.status_code == 404

    redeem_response = client.post(
        f"/rewards/{reward_id}/redeem",
        headers=second_user_header
    )

    assert redeem_response.status_code == 404

    delete_response = client.delete(
        f"/rewards/{reward_id}",
        headers=second_user_header
    )

    assert delete_response.status_code == 404