from app.repositories.incident_repository import IncidentRepository

class PostgresIncidentRepository(IncidentRepository):
   def __init__(self, db_session):
      self.db = db_session

   def save(self, incident_data: dict):
      print("Saving to PostgreSQL...")
      return {"id": 1, **incident_data}

   def get_by_id(self, incident_id: int):
      pass