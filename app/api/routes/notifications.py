from fastapi import (
    APIRouter,
    Request,
    HTTPException
)

from app.db.database import SessionLocal

from app.models.notification import Notification

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get("/")
def get_notifications(
    request: Request
):

    db = SessionLocal()

    try:

        current_user = request.state.user

        notifications = db.query(Notification).filter(
            Notification.user_id == current_user.id
        ).all()

        return notifications

    finally:

        db.close()


@router.patch("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    request: Request
):

    db = SessionLocal()

    try:

        current_user = request.state.user

        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ).first()

        if not notification:

            raise HTTPException(
                status_code=404,
                detail="Notification not found"
            )

        notification.is_read = True

        db.commit()

        return {
            "message": "Notification marked as read"
        }

    finally:

        db.close()