from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from services.security_service import security_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Validates the provided JWT token and extracts the user identity (sub).
    Returns the user ID (string). Does NOT query the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = security_service.decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
        
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
        
    return user_id
