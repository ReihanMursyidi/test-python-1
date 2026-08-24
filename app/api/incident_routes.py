from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, status
from typing import List, Optional
from app.schemas.incident_schema import IncidentCreate, IncidentResponse, IncidentUpdateStatus, IncidentStatus, IncidentPriority
from app.core.dependencies import get_incident_service
from app.services.notification_service import send_notification_async 
from app.services.incident_service import IncidentService

router = APIRouter(prefix="/incidents", tags=["Incidents"])

# 1. Create Incident
@router.post("", response_model=IncidentResponse, status_code=201)
def create_incident(
   payload: IncidentCreate,
   background_tasks: BackgroundTasks,
   service: IncidentService = Depends(get_incident_service)
):
   incident = service.create_incident(
      title=payload.title,
      description=payload.description,
      reported_by=payload.reported_by
   )
   background_tasks.add_task(send_notification_async, incident.id)

   return incident

# 2. Get Incident by ID
@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
   incident_id: int, 
   service: IncidentService = Depends(get_incident_service)
):
   incident = service.get_incident_by_id(incident_id)
   if not incident:
      raise HTTPException(status_code=404, detail="Incident not found")
   return incident

# 3. List Incidents (Filter & Pagination)[cite: 1]
@router.get("", response_model=List[IncidentResponse])
def list_incidents(
   status: Optional[IncidentStatus] = Query(None, description="Filter by status"),
   priority: Optional[IncidentPriority] = Query(None, description="Filter by priority"),
   limit: int = Query(10, ge=1, le=100),
   offset: int = Query(0, ge=0),
   service: IncidentService = Depends(get_incident_service)
):
   status_val = status.value if status else None
   priority_val = priority.value if priority else None
   incidents = service.list_incidents(status_val, priority_val, limit, offset)
   return incidents

# 4. Update Status[cite: 1]
@router.patch("/{incident_id}/status", response_model=IncidentResponse)
def update_incident_status(
   incident_id: int, 
   payload: IncidentUpdateStatus,
   service: IncidentService = Depends(get_incident_service)
):

   updated_incident = service.update_status(incident_id, payload.status.value)
   if not updated_incident:
      raise HTTPException(status_code=404, detail="Incident not found")
   return updated_incident