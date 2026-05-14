from fastapi import APIRouter, HTTPException

from app.db.database import SessionLocal
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest
)

from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(payload: RegisterRequest):

    db = SessionLocal()

    try:

        existing = db.query(User).filter(
            User.email == payload.email
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="User already exists"
            )

        hashed_password = hash_password(
            payload.password
        )

        user = User(
            name=payload.name,
            email=payload.email,
            hashed_password=hashed_password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "message": "User registered successfully",
            "user_id": user.id
        }

    finally:
        db.close()


@router.post("/login")
def login(payload: LoginRequest):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == payload.email
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        is_valid_password = verify_password(
            payload.password,
            user.hashed_password
        )

        if not is_valid_password:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token({
            "user_id": user.id,
            "email": user.email
        })

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }

    finally:
        db.close()