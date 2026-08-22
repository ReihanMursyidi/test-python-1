import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.dependencies import get_incident_service
from unittest.mock import MagicMock

client = TestClient(app)

def override_get_incident_service():
   mock_service = MagicMock()
   # Setup mock untuk mengembalikan None (mensimulasikan tidak ditemukan)
   mock_service.get_incident_by_id.return_value = None
   return mock_service

# Mengganti dependency asli dengan mock khusus untuk test ini
app.dependency_overrides[get_incident_service] = override_get_incident_service

def test_get_incident_not_found():
   # Verifikasi 3: Incident not found harus mengembalikan 404[cite: 1]
   response = client.get("/incidents/999")
   assert response.status_code == 404
   assert response.json()["detail"] == "Incident not found"

def test_update_invalid_status():
   # Verifikasi 4: Invalid status menghasilkan HTTP status yang sesuai (422 Unprocessable Entity dari Pydantic)[cite: 1]
   response = client.patch("/incidents/1/status", json={"status": "INVALID_STATUS_NAME"})
   
   # FastAPI/Pydantic secara otomatis memblokir nilai Enum yang tidak valid dengan status 422
   assert response.status_code == 422