from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from core.config import settings
from core.database import get_db
from models import orm_models, pydantic_schemas
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

@router.post("/sync", response_model=pydantic_schemas.UserResponse)
def sync_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    db: Session = Depends(get_db)
):
    """
    Decodes the Google JWT from NextAuth. 
    If the user doesn't exist in our SQL DB, create them. 
    If they do, return their profile.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        user_id = payload.get("sub")
        email = payload.get("email")
        name = payload.get("name")
        picture = payload.get("picture")

        if not user_id or not email:
            raise HTTPException(status_code=400, detail="Invalid token payload")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    # Check if user already exists
    user = db.query(orm_models.User).filter(orm_models.User.id == user_id).first()

    if not user:
        # Auto-signup: Create user record in PostgreSQL
        user = orm_models.User(
            id=user_id,
            email=email,
            name=name,
            picture=picture
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user