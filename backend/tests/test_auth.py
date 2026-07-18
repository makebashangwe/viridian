def test_root_route(client):
    response = client.get("/")

    #assert = "This Condition must be true for the test to pass."
    assert response.status_code == 200
    assert response.json() == {
        "message": "Viridian API is running"
    }

def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "pytest@example.com",
            "username": "pytestuser",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["email"] == "pytest@example.com"
    assert response_data["username"] == "pytestuser"
    assert "id" in response_data
    assert "password" not in response_data
    assert "password_hash" not in response_data

def test_register_duplicate_email(client):
    user_data = {
        "email": "duplicate@example.com",
        "username": "firstuser",
        "password": "password123"
    }

    first_response = client.post(
        "/auth/register",
        json=user_data
    )

    second_response = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "seconduser",
            "password": "password123"
        }
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email already exists."

def test_register_duplicate_username(client):
 
    first_response = client.post(
        "/auth/register",
        json =  {
        "email": "first@example.com",
        "username": "duplicateuser",
        "password": "password123"
    }
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json = {
            "email": "second@example.com",
            "username": "duplicateuser",
            "password": "password123"
        }
    )
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Username already exists."

def test_login_successful(client):
    register_response = client.post(
        "/auth/register",
        json={
            "email": "pytest@example.com",
            "username": "pytestuser",
            "password": "password123"
        }
    )
    assert register_response.status_code == 201

    login_response = client.post(
    "/auth/login",
    json = {
            "email": "pytest@example.com",
            "password": "password123"
            }
    )

    login_data = login_response.json()
    assert login_response.status_code == 200
    assert isinstance(login_data["access_token"],str) 
    assert len(login_data["access_token"])>0
    assert login_data["token_type"] == "bearer"
 
def test_swagger_token_successful(client):
    register_response = client.post(
        "/auth/register",
        json={
            "email": "swagger@example.com",
            "username": "swaggeruser",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    token_response = client.post(
        "/auth/token",
        data={
            "username": "swagger@example.com",
            "password": "password123"
        }
    )

    token_data = token_response.json()

    assert token_response.status_code == 200
    assert isinstance(token_data["access_token"], str)
    assert len(token_data["access_token"]) > 0
    assert token_data["token_type"] == "bearer"


def test_login_wrong_password(client):
    register_response = client.post(
        "/auth/register",
        json={
            "email": "pytest@example.com",
            "username": "pytestuser",
            "password": "password123"
        }
    )
    assert register_response.status_code == 201

    login_response = client.post(
    "/auth/login",
    json = {
            "email": "pytest@example.com",
            "password": "password456" #wrong password
            }
    )

    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Invalid Email or Password."

def test_me_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401

def test_login_unknown_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "missing@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Email or Password."


def test_read_current_user(client):
    register_response = client.post(
        "/auth/register",
        json={
            "email": "me@example.com",
            "username": "meuser",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "me@example.com",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["email"] == "me@example.com"
    assert response_data["username"] == "meuser"
    assert "id" in response_data

def test_swagger_token_wrong_password(client):
    register_response = client.post(
        "/auth/register",
        json={
            "email": "swaggerfail@example.com",
            "username": "swaggerfailuser",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    token_response = client.post(
        "/auth/token",
        data={
            "username": "swaggerfail@example.com",
            "password": "wrongpassword"
        }
    )

    assert token_response.status_code == 401
    assert token_response.json()["detail"] == "Invalid email or password."
    assert token_response.headers["www-authenticate"] == "Bearer"
    
def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "not-an-email",
            "username": "invalidemailuser",
            "password": "password123"
        }
    )

    assert response.status_code == 422


def test_register_short_password(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "shortpassword@example.com",
            "username": "shortpassworduser",
            "password": "short"
        }
    )

    assert response.status_code == 422