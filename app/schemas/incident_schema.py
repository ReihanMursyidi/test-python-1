from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from datetime import datetime
from typing import Optional

# Validasi Status dan Priority
class IncidentStatus(str, Enum):
   OPEN = "OPEN"
   IN_PROGRESS = "IN_PROGRESS"
   RESOLVED = "RESOLVED"
   CLOSED = "CLOSED"

class IncidentPriority(str, Enum):
   HIGH = "HIGH"
   MEDIUM = "MEDIUM"
   LOW = "LOW"

class IncidentCreate(BaseModel):
   title: str
   description: str
   reported_by: EmailStr

class IncidentUpdateStatus(BaseModel):
   status: IncidentStatus

class IncidentResponse(BaseModel):
   id: int
   title: str
   description: str
   reported_by: str
   status: IncidentStatus
   priority: IncidentPriority
   category: str
   created_at: datetime

   model_config = ConfigDict(from_attributes=True)