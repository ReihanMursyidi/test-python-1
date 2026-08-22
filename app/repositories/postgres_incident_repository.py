from app.repositories.incident_repositories import IncidentRepository

class PostgresIncidentRepository(IncidentRepository):
   def __init__(self, db_session):
      self.db_session = db_session

   def save(self, incident):
      self.db_session.add(incident)
      self.db_session.commit()
      self.db_session.refresh(incident)
      return incident

   def get_by_id(self, incident_id: int):
      pass