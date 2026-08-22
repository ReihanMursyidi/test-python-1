import pytest
from unittest.mock import MagicMock
from app.services.incident_service import IncidentService

@pytest.fixture
def mock_repo():
   return MagicMock()

@pytest.fixture
def mock_classifier():
   return MagicMock()

@pytest.fixture
def incident_service(mock_repo, mock_classifier):
   return IncidentService(repository=mock_repo, classifier=mock_classifier)

def test_incident_creation_and_interactions(incident_service, mock_repo, mock_classifier):
   # Setup mock return values
   mock_classifier.predict_category.return_value = "NETWORK"
   mock_repo.save.return_value = {"id": 1, "status": "OPEN", "category": "NETWORK"}

   # Eksekusi fungsi
   result = incident_service.create_incident(
      title="Wifi disconnected",
      description="Cannot connect to office wifi",
      reported_by="user@example.com"
   )

   # Verifikasi 7: Classifier dipanggil ketika incident dibuat
   mock_classifier.predict_category.assert_called_once_with(
      "Wifi disconnected", "Cannot connect to office wifi"
   )

   # Verifikasi 5: Repository/service interaction (pastikan save dipanggil)
   mock_repo.save.assert_called_once()
   saved_data = mock_repo.save.call_args[0][0] # Mengambil argumen pertama dari pemanggilan save
   
   assert saved_data["category"] == "NETWORK"
   assert saved_data["reported_by"] == "user@example.com"
   
   # Verifikasi 2: Incident creation berhasil[cite: 1]
   assert result["id"] == 1
   assert result["category"] == "NETWORK"