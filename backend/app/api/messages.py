from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.message import Message
from app.models.task import Task, TaskStatus
from app.models.user import User
from backend.app.schemas.messages import MessageCreate


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
    db.commit()
    db.refresh(new_message)

    return new_message