from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import DATABASE_URL
from app.repositories.incident_repositories import PostgresIncidentRepository
from app.services.incident_service import IncidentService
from app.services.classification_service import ClassificationService

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()

def get_incident_service(db: Session = Depends(get_db)):
   # Inisialisasi DB session / repository
   repository = PostgresIncidentRepository(db)
   classifier = ClassificationService()

   return IncidentService(repository=repository, classifier=classifier)