import pytest
from unittest.mock import MagicMock
from app.services.incident_service import IncidentService

@pytest.fixture
def incident_service():
   mock_repo = MagicMock()
   mock_classifier = MagicMock()
   
   mock_classifier.predict.return_value = "DATABASE"
   
   return IncidentService(repository=mock_repo, classifier=mock_classifier)

def test_priority_high_when_server_down(incident_service):
   incident_service.create_incident(
      title="Server down",
      description="Production is not accessible",
      reported_by="user@example.com"
   )

   args, _ = incident_service.repository.save.call_args
   saved_incident = args[0]
   
   assert saved_incident.priority == "HIGH"

def test_priority_medium_when_login_error(incident_service):
   incident_service.create_incident(
      title="Login Issue",
      description="I got an error when logging in",
      reported_by="user@example.com"
   )
   
   args, _ = incident_service.repository.save.call_args
   saved_incident = args[0]
   
   assert saved_incident.priority == "MEDIUM"

def test_priority_low_for_general_questions(incident_service):
   incident_service.create_incident(
      title="Need new mouse",
      description="My mouse is broken",
      reported_by="user@example.com"
   )
   
   args, _ = incident_service.repository.save.call_args
   saved_incident = args[0]
   
   assert saved_incident.priority == "LOW"