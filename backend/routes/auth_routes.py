"""
Auth routes – Register, login, and user profile endpoints.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User, UserRole
from schemas.auth_schema import UserRegister, UserLogin, TokenResponse, UserResponse
from services.auth_service import (
    hash_password,
    create_access_token,
    authenticate_user,
    get_user_by_email,
)
from services.email_service import send_welcome_email
from dependencies.auth_dependency import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    payload: UserRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Register a new user.

    **Sample request:**
    ```json
    {
        "email": "priya@example.com",
        "password": "securepass123",
        "role": "volunteer"
    }
    ```
    """
    # Check if email already exists
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create user
    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=UserRole(payload.role.value),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info("Registered user id=%d email=%s role=%s", user.id, user.email, user.role.value)

    # Send welcome email in background
    background_tasks.add_task(send_welcome_email, user.email, user.role.value)

    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.

    **Sample request:**
    ```json
    {
        "email": "priya@example.com",
        "password": "securepass123"
    }
    ```

    **Sample response:**
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIs...",
        "token_type": "bearer",
        "role": "volunteer",
        "message": "Login successful"
    }
    ```
    """
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value}
    )

    logger.info("User logged in: %s (role=%s)", user.email, user.role.value)

    return TokenResponse(
        access_token=access_token,
        role=user.role.value,
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user's profile.
    Requires Bearer token in Authorization header.
    """
    return current_user
