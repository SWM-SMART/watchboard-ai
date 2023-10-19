from fastapi.testclient import TestClient

def test_question(client: TestClient) -> None:
    response = client.post("/question")
    assert response.status_code() == 200