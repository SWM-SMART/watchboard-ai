from fastapi.testclient import TestClient

def test_pdf_keywords_extraction(client: TestClient) -> None:
    data = {"key": DUMMY_PDF_PATH, "db": "s3"}
    response = client.post("/keywords", json=data)
    assert response.status_code() == 200

def test_bad_pdf_keywords_extraction(client: TestClient) -> None:
    data = {"key": "1234", "db": "s3"}
    response = client.post("/keywords", json=data)
    assert response.status_code() == 404