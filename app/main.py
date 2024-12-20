from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from .models import Client, Project, Base  # Import models from models.py
from pydantic import BaseModel

# Database Configuration
DATABASE_URL = "sqlite:///./ClientPro.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Tables
Base.metadata.create_all(bind=engine)

# FastAPI Application
app = FastAPI()

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Dependency for Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Models
class ClientCreate(BaseModel):
    name: str
    email: str
    phone: str
    company: str

class ProjectCreate(BaseModel):
    title: str
    description: str
    status: str = "Pending"
    client_id: int

# Routes for Clients
@app.post("/clients/")
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    try:
        new_client = Client(
            name=client.name,
            email=client.email,
            phone=client.phone,
            company=client.company,
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists.")

@app.get("/clients/")
def read_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@app.get("/clients/{client_id}/")
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")
    return client

@app.get("/clients/{client_id}/projects/")
def read_client_projects(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")
    return client.projects

@app.delete("/clients/{client_id}/")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")
    db.delete(client)
    db.commit()
    return {"detail": "Client deleted successfully."}

# Routes for Projects
@app.post("/projects/")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == project.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")
    new_project = Project(
        title=project.title,
        description=project.description,
        status=project.status,
        client_id=project.client_id,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@app.get("/projects/")
def read_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

@app.get("/projects/{project_id}/")
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project

@app.delete("/projects/{project_id}/")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    db.delete(project)
    db.commit()
    return {"detail": "Project deleted successfully."}