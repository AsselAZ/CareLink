from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_senior
from app.db.database import get_db
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(require_senior),
    db: Session = Depends(get_db),
):
    # Der eingeloggte Senior wird automatisch als Besitzer gesetzt
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        category=task_data.category.value,
        status=TaskStatus.OPEN.value,
        task_date=task_data.task_date,
        start_time=task_data.start_time,
        end_time=task_data.end_time,
        senior_id=current_user.id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "category": new_task.category,
        "status": new_task.status,
        "task_date": new_task.task_date,
        "start_time": new_task.start_time,
        "end_time": new_task.end_time,
        "senior_id": new_task.senior_id,
        "helper_id": new_task.helper_id,
    }