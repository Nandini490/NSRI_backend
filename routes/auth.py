from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from services.database_service import create_user, get_user_by_email
from services.security_service import security_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class UserSignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(request: UserSignupRequest):
    try:
        # 1. Check if email already exists
        existing_user = get_user_by_email(request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered."
            )
            
        # 2. Hash the password
        password_hash = security_service.get_password_hash(request.password)
        
        # 3. Create the user
        new_user = create_user(
            name=request.name,
            email=request.email,
            password_hash=password_hash
        )
        
        # 4. Return success response (DO NOT return password_hash)
        return {
            "message": "User created successfully",
            "user_id": new_user["user_id"],
            "name": new_user["name"],
            "email": new_user["email"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during signup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during user registration."
        )

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(request: UserLoginRequest):
    # 1. Find user by email
    user = get_user_by_email(request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 2. Verify password
    if not security_service.verify_password(request.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Create JWT access token
    user_id = str(user.get("_id", ""))
    access_token = security_service.create_access_token(
        data={"sub": user_id}
    )
    
    # 4. Return token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
