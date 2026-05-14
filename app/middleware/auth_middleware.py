from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError

from app.db.database import SessionLocal
from app.models.user import User

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


PUBLIC_ROUTES = [
    "/",
    "/auth/login",
    "/auth/register",
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc"
]

async def auth_middleware(request: Request, call_next):

    if request.url.path in PUBLIC_ROUTES:
        return await call_next(request)

    authorization = request.headers.get("Authorization")

    if not authorization:

        return JSONResponse(
            status_code=401,
            content={
                "detail": "Authorization header missing"
            }
        )

    try:

        parts = authorization.split()

        if len(parts) != 2:

            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid authorization format"
                }
            )

        scheme, token = parts

        if scheme.lower() != "bearer":

            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid authentication scheme"
                }
            )

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if not user_id:

            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid token payload"
                }
            )

        db = SessionLocal()

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        db.close()

        if not user:

            return JSONResponse(
                status_code=401,
                content={
                    "detail": "User not found"
                }
            )


        request.state.user = user

        response = await call_next(request)

        return response

    except JWTError:

        return JSONResponse(
            status_code=401,
            content={
                "detail": "Invalid or expired token"
            }
        )