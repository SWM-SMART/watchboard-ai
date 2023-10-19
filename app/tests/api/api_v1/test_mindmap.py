from fastapi.testclient import TestClient

def test_mindmap(client: TestClient) -> None:
    data = {
        "key": DUMMY_PDF_PATH,
	    "db": "s3",
	    "keywords": ["abc", "def", "ghi"],
	    "documentId": DUMMY_MONGO_DB_ID
    }
    response = client.post("/mindmap", json=data)
    assert response.status_code() == 200
    