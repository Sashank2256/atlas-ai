def create_conversation(client, auth_headers):
    response = client.post(
        "/api/v1/conversations",
        headers=auth_headers,
        json={
            "title": "Message Test",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_send_message(client, auth_headers):
    conversation_id = create_conversation(
        client,
        auth_headers,
    )

    response = client.post(
        f"/api/v1/messages/{conversation_id}",
        headers=auth_headers,
        json={
            "content": "Hello Atlas!",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["conversation_id"] == conversation_id
    assert body["role"] == "assistant"
    assert isinstance(body["content"], str)
    assert len(body["content"]) > 0
    assert "id" in body
    assert "created_at" in body


def test_list_messages(client, auth_headers):
    conversation_id = create_conversation(
        client,
        auth_headers,
    )

    client.post(
        f"/api/v1/messages/{conversation_id}",
        headers=auth_headers,
        json={
            "content": "Hello!",
        },
    )

    response = client.get(
        f"/api/v1/messages/{conversation_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    messages = response.json()

    assert isinstance(messages, list)
    assert len(messages) >= 2

    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_send_message_invalid_conversation(
    client,
    auth_headers,
):
    response = client.post(
        "/api/v1/messages/999999",
        headers=auth_headers,
        json={
            "content": "Hello",
        },
    )

    assert response.status_code == 404


def test_list_messages_invalid_conversation(
    client,
    auth_headers,
):
    response = client.get(
        "/api/v1/messages/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_send_empty_message(
    client,
    auth_headers,
):
    conversation_id = create_conversation(
        client,
        auth_headers,
    )

    response = client.post(
        f"/api/v1/messages/{conversation_id}",
        headers=auth_headers,
        json={
            "content": "",
        },
    )

    assert response.status_code in (201, 422)