from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.rating import Rating
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.rating import RatingCreate


router = APIRouter(
    prefix="/tasks",
    tags=["Ratings"],
)


@router.post("/{task_id}/rating", status_code=status.HTTP_201_CREATED)
def create_rating(
    task_id: int,
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task wurde nicht gefunden.",
        )

    if task.status != TaskStatus.DONE.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nur erledigte Tasks können bewertet werden.",
        )

    if current_user.id == task.senior_id:
        reviewed_user_id = task.helper_id

    elif current_user.id == task.helper_id:
        reviewed_user_id = task.senior_id

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sie waren an diesem Task nicht beteiligt.",
        )

    if reviewed_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Für diesen Task gibt es keinen Helfer.",
        )

    existing_rating = db.scalar(
        select(Rating).where(
            Rating.task_id == task.id,
            Rating.reviewer_id == current_user.id,
        )
    )

    if existing_rating:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sie haben diesen Task bereits bewertet.",
        )

    new_rating = Rating(
        task_id=task.id,
        reviewer_id=current_user.id,
        reviewed_user_id=reviewed_user_id,
        stars=rating_data.stars,
        comment=rating_data.comment,
    )

    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    return new_rating