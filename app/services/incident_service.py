from app.repositories.incident_repositories import IncidentRepository
from app.services.classification_service import ClassificationService
from app.models.incident_model import Incident

class IncidentService:
   def __init__(
      self, 
      repository: IncidentRepository, 
      classifier: ClassificationService
   ):
      self.repository = repository
      self.classifier = classifier

   def create_incident(self, title: str, description: str, reported_by: str):
      text_to_check = f"{title} {description}".lower()
      if any(keyword in text_to_check for keyword in ["server down", "database down", "payment failure", "security breach"]):
         priority = "HIGH"
      elif any(keyword in text_to_check for keyword in ["login", "slow", "timeout", "error"]):
         priority = "MEDIUM"
      else:
         priority = "LOW"

      category = self.classifier.predict(text_to_check)
      
      new_incident_data = Incident(
         title=title,
         description=description,
         reported_by=reported_by,
         priority=priority,
         category=category,
         status="OPEN"
      )

      saved_incident = self.repository.save(new_incident_data)
      return saved_incident

   def list_incidents(self, status: str = None, priority: str = None, limit: int = 10, offset: int = 0):
      return self.repository.get_all(
         status=status, 
         priority=priority, 
         limit=limit, 
         offset=offset
      )