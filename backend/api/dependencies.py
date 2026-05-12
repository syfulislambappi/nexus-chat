from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from core.config import settings
from core.database import get_db
from models import orm_models

# This helper will look for the "Authorization: Bearer <token>" header
security = HTTPBearer()

def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security), 
    db: Session = Depends(get_db)
):
    """
    Decodes the JWT token sent from NextAuth and retrieves the user 
    from the PostgreSQL database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token using the SECRET_KEY shared with the frontend
        payload = jwt.decode(
            token.credentials, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # NextAuth typically puts the user ID in the 'sub' field
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    # Check if the user exists in our SQL database
    user = db.query(orm_models.User).filter(orm_models.User.id == user_id).first()
    
    if user is None:
        # If the user is authenticated via Google but not in our DB yet, 
        # we will handle the "auto-signup" in the auth route later.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in system"
        )
        
    return user