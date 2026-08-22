from fastapi import FastAPI
from api import incident_routes

app = FastAPI(
   title = "Incident Management API",
   description = "IT Support Incident Management Service"
)

app.include_router(incident_routes.router)

@app.get("/")
def root():
   return { "message": "Welcome" }