import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_invalid_status_rejected():
    # Menguji Verifikasi 4: Invalid status menghasilkan HTTP 422 Unprocessable Entity
    response = client.patch("/incidents/1/status?status=INVALID_STATUS_NAME")
    
    # FastAPI/Pydantic secara otomatis memblokir nilai Enum yang tidak valid
    assert response.status_code == 422