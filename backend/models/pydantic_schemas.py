from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

# --- Base Schemas (Shared) ---
class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None

# --- User Schemas ---
class UserCreate(UserBase):
    id: str  # The Google 'sub' ID

class UserResponse(UserBase):
    id: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Chat Schemas ---
class ChatMessageCreate(BaseModel):
    session_id: str
    content: str

class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Document Schemas ---
class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    storage_url: str
    upload_timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Combined History Schema ---
class ChatSessionResponse(BaseModel):
    session_id: str
    messages: List[ChatMessageResponse]