import uuid


def test_register_user(client):
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"
    username = f"user-{uuid.uuid4().hex[:8]}"

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "Password@123",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["username"] == username
    assert body["email"] == email
    assert "id" in body


def test_register_duplicate_username(client):
    username = f"user-{uuid.uuid4().hex[:8]}"

    client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": f"{uuid.uuid4().hex}@example.com",
            "password": "Password@123",
        },
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": f"{uuid.uuid4().hex}@example.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


def test_register_duplicate_email(client):
    email = f"{uuid.uuid4().hex}@example.com"

    client.post(
        "/api/v1/auth/register",
        json={
            "username": f"user-{uuid.uuid4().hex[:8]}",
            "email": email,
            "password": "Password@123",
        },
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": f"user-{uuid.uuid4().hex[:8]}",
            "email": email,
            "password": "Password@123",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"


def test_login_success(client):
    username = f"user-{uuid.uuid4().hex[:8]}"
    email = f"{uuid.uuid4().hex}@example.com"
    password = "Password@123"

    client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "bearer"


def test_login_invalid_password(client):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "unknown",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"