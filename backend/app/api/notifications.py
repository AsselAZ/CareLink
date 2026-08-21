from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.notification import Notification
from app.models.user import User


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get("/me")
def get_my_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notifications = db.scalars(
        select(Notification).where(
            Notification.user_id == current_user.id
        )
    ).all()

    return notifications

# Mark a notification as read
@router.post("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notification = db.get(Notification, notification_id)

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Benachrichtigung wurde nicht gefunden.",
        )
# prüfen ob die nachricht an den eingeloggten user gehört, sonst 403
##Autorisierungsprüfung
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Diese Benachrichtigung gehört nicht zu Ihnen.",
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification

# Get unread notifications for the current user
@router.get("/unread")
def get_unread_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notifications = db.scalars(
        select(Notification).where(
            Notification.user_id == current_user.id,
            Notification.is_read == False,
        )
    ).all()

    return notifications