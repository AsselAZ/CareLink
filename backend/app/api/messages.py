from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.message import Message
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.messages import MessageCreate
from app.models.notification import Notification


router = APIRouter(
    prefix="/tasks",
    tags=["Messages"],
)

# Send a message related to a specific task
@router.post("/{task_id}/messages", status_code=status.HTTP_201_CREATED)
def send_message(
    task_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task wurde nicht gefunden.",
        )

    # Chat ist erst sinnvoll, wenn ein Helper zugeordnet ist
    if task.helper_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Für diesen Task gibt es noch keinen Helfer.",
        )

    # Nur Senior oder zugeordneter Helper dürfen schreiben
    if (
        current_user.id != task.senior_id
        and current_user.id != task.helper_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sie sind nicht an diesem Task beteiligt.",
        )

    # Kein Chat mehr für stornierte Tasks
    if task.status == TaskStatus.CANCELLED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Für einen stornierten Task können keine Nachrichten gesendet werden.",
        )

    new_message = Message(
        task_id=task.id,
        sender_id=current_user.id,
        message=message_data.message,
    )

    db.add(new_message)
    # Bestimmen, wer die Nachricht erhalten soll
    if current_user.id == task.senior_id:
        recipient_id = task.helper_id
    else:
        recipient_id = task.senior_id

    # Empfänger über die neue Nachricht informieren
    notification = Notification(
        user_id=recipient_id,
        message=f"Sie haben eine neue Nachricht zum Task '{task.title}'.",
    )

    db.add(notification)
    db.commit()
    db.refresh(new_message)

    return new_message


# Get all messages-verlauf related to a specific task
@router.get("/{task_id}/messages")
def get_messages(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task wurde nicht gefunden.",
        )

    # Nur Senior und zugeordneter Helper dürfen den Chat lesen
    if (
        current_user.id != task.senior_id
        and current_user.id != task.helper_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sie sind nicht an diesem Task beteiligt.",
        )

    messages = db.scalars(
        select(Message)
        .where(Message.task_id == task_id)
        .order_by(Message.created_at.asc())
    ).all()

    return messages