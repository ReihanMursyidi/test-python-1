from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.incident_model import Incident

class IncidentRepository(ABC):
    @abstractmethod
    def save(self, incident_data: Incident) -> Incident:
        pass
    
    @abstractmethod
    def get_by_id(self, incident_id: int)-> Optional[Incident]:
        pass

    @abstractmethod
    def get_all(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None, 
        limit: int = 10, 
        offset: int = 0
    ) -> List[Incident]:
        pass

class PostgresIncidentRepository(IncidentRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, incident_data: Incident) -> Incident:
        self.db.add(incident_data)
        self.db.commit()
        self.db.refresh(incident_data)
        return incident_data

    def get_by_id(self, incident_id: int) -> Optional[Incident]:
        return self.db.query(Incident).filter(Incident.id == incident_id).first()

    def get_all(
        self, 
        status: Optional[str] = None, 
        priority: Optional[str] = None, 
        limit: int = 10, 
        offset: int = 0
    )-> List[Incident]:
        query = self.db.query(Incident)

        if status:
            query = query.filter(Incident.status == status)
        if priority:
            query = query.filter(Incident.priority == priority)

        return query.offset(offset).limit(limit).all()