from app.services.llm_service import llm_service


def fake_chat(messages):
    return "Mock AI Response"


def create_conversation(client, auth_headers):
    response = client.post(
        "/api/v1/conversations",
        headers=auth_headers,
        json={
            "title": "Mock Chat",
        },
    )

    return response.json()["id"]


def test_mock_ai(monkeypatch, client, auth_headers):
    monkeypatch.setattr(
        llm_service,
        "chat",
        fake_chat,
    )

    conversation_id = create_conversation(
        client,
        auth_headers,
    )

    response = client.post(
        f"/api/v1/messages/{conversation_id}",
        headers=auth_headers,
        json={
            "content": "Hello",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["role"] == "assistant"
    assert body["content"] == "Mock AI Response"