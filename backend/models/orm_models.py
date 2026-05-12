from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class User(Base):
    __tablename__ = "users"

    # We use the Google Subject ID (sub) as the primary key string
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    picture = Column(String)  # Store Google profile pic URL
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships: If a user is deleted, their chats and docs should follow (cascading)
    chats = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    session_id = Column(String, index=True, nullable=False)  # Groups messages into conversations
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chats")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String)  # .pdf, .docx, .pptx
    
    # This stores the DigitalOcean Spaces Object Key or URL
    storage_url = Column(String, nullable=False)
    
    # Store the Pinecone namespace or metadata filter ID to delete vectors later
    vector_namespace = Column(String, unique=True, index=True) 
    
    upload_timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="documents")