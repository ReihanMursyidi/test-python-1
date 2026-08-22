from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Index
from sqlalchemy.orm import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class IncidentStatus(str, enum.Enum):
   OPEN = "OPEN"
   IN_PROGRESS = "IN_PROGRESS"
   RESOLVED = "RESOLVED"
   CLOSED = "CLOSED"

class Incident(Base):
   __tablename__ = "incidents"

   id = Column(Integer, primary_key=True)
   title = Column(String(255), nullable=False)
   description = Column(Text, nullable=False)
   reported_by = Column(String(255), nullable=False)
   status = Column(Enum(IncidentStatus), default=IncidentStatus.OPEN, nullable=False)
   priority = Column(String(50))
   category = Column(String(50))
   created_at = Column(DateTime, default=datetime.utcnow)
   updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

   __table_args__ = (
      Index('idx_incidents_status_created_at', 'status', 'created_at'),
   )