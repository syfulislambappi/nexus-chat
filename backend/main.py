from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import engine, Base
from api import auth_routes

# Critical: Import models so SQLAlchemy "sees" them before creating tables
from models import orm_models 

# Create database tables on startup
# Note: In a production environment, you'd use Alembic migrations,
# but for our build-out, this is the most direct way to initialize.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Backend for NexusRAG - Advanced Multi-Modal RAG Platform"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows your Next.js frontend (e.g., localhost:3000) to communicate with this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # For production, replace "*" with your specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    """
    Basic endpoint to verify the server is running.
    """
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": "1.0.0"
    }

app.include_router(auth_routes.router)