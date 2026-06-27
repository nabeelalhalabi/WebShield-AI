from fastapi.testclient import TestClient
from app.main import app

def main() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/health")
    response.raise_for_status()
    print(response.json())

if __name__ == "__main__":
    main()
