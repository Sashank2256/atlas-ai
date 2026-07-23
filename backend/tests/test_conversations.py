import uuid

def test_create_conversation(client, auth_headers):
    response = client.post(
        "/api/v1/conversations",
        headers=auth_headers,
        json={
            "title": "My First Chat",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["title"] == "My First Chat"
    assert "id" in body


def test_list_conversations(client, auth_headers):
    client.post(
        "/api/v1/conversations",
        headers=auth_headers,
        json={
            "title": "Conversation One",
        },
    )

    response = client.get(
        "/api/v1/conversations",
        headers=auth_headers,
    )

    assert response.status_code == 200

    conversations = response.json()

    assert isinstance(conversations, list)
    assert len(conversations) >= 1


def test_get_conversation_by_id(client, auth_headers):
    create_response = client.post(
        "/api/v1/conversations",
        headers=auth_headers,
        json={
            "title": "Get Conversation Test",
        },
    )

    conversation = create_response.json()

    response = client.get(
        f"/api/v1/conversations/{conversation['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == conversation["id"]
    assert body["title"] == "Get Conversation Test"


def test_update_conversation(client, auth_headers):
    create_response = client.post(
        "/api/v1/conversations",
        headers=auth_headers,
        json={
            "title": "Old Title",
        },
    )

    conversation = create_response.json()

    response = client.patch(
        f"/api/v1/conversations/{conversation['id']}",
        headers=auth_headers,
        json={
            "title": "New Title",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["title"] == "New Title"


def test_delete_conversation(client, auth_headers):
    create_response = client.post(
        "/api/v1/conversations",
        headers=auth_headers,
        json={
            "title": "Delete Me",
        },
    )

    conversation = create_response.json()

    response = client.delete(
        f"/api/v1/conversations/{conversation['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_get_non_existing_conversation(client, auth_headers):
    response = client.get(
        "/api/v1/conversations/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404