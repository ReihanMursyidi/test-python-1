from abc import ABC, abstractmethod

class IncidentRepository(ABC):
    @abstractmethod
    def save(self, incident_data: dict):
        pass
    
    @abstractmethod
    def get_by_id(self, incident_id: int):
        pass