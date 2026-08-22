from app.repositories.incident_repository import IncidentRepository
from app.services.classification_service import ClassificationService

class IncidentService:
   def __init__(
      self, 
      repository: IncidentRepository, 
      classifier: ClassificationService
   ):
      self.repository = repository
      self.classifier = classifier

   def create_incident(self, title: str, description: str, reported_by: str):
      # 1. Tentukan kategori via ML (Business Logic)
      category = self.classifier.predict_category(title, description)
      
      # 2. Siapkan data
      incident_data = {
         "title": title,
         "description": description,
         "reported_by": reported_by,
         "status": "OPEN",
         "category": category,
      }
      
      saved_incident = self.repository.save(incident_data)
      return saved_incident