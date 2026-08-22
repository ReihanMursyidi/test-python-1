from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import DATABASE_URL
from app.repositories.postgres_incident_repository import PostgresIncidentRepository
from app.services.classification_service import ClassificationService
from app.services.incident_service import IncidentService

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()

def get_incident_service(db: Session = Depends(get_db)) -> IncidentService:
   # Inisialisasi DB session / repository
   repo = PostgresIncidentRepository(db_session=db)
   classifier = ClassificationService()

   return IncidentService(repository=repo, classifier=classifier)