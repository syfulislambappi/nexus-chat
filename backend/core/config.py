from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NexusRAG API"
    
    # Database
    DATABASE_URL: str 
    
    # Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    
    # AI Services
    OPENAI_ROUTER_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENV: str
    PINECONE_INDEX_NAME: str

    # DigitalOcean Spaces
    DO_SPACES_KEY: str
    DO_SPACES_SECRET: str
    DO_SPACES_ENDPOINT: str
    DO_SPACES_BUCKET: str

    class Config:
        env_file = ".env"

# Instantiate the settings so it can be imported across the app
settings = Settings()