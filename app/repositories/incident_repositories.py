from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.incident_model import Incident

class IncidentRepository(ABC):
    @abstractmethod
    def save(self, incident_data: dict):
        pass
    
    @abstractmethod
    def get_by_id(self, incident_id: int):
        pass

    @abstractmethod
    def get_all(self, status: str = None, priority: str = None, limit: int = 10, offset: int = 0):
        pass

class PostgresIncidentRepository(IncidentRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, incident_data: dict):
        incident = Incident(**incident_data)
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        return incident

    def get_by_id(self, incident_id: int):
        return self.db.query(Incident).filter(Incident.id == incident_id).first()

    def get_all(self, status: str = None, priority: str = None, limit: int = 10, offset: int = 0):
        query = self.db.query(Incident)

        if status:
            query = query.filter(Incident.status == status)
        if priority:
            query = query.filter(Incident.priority == priority)

        return query.offset(offset).limit(limit).all()