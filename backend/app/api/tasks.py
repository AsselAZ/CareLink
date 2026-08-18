from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_senior
from app.db.database import get_db
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskCategory

from app.models.task_details import (
    ShoppingDetails,
    AppointmentDetails,
    FurnitureDetails,
    CraftDetails,
)


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
    # Zuerst wird der allgemeine Task erstellt
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

    # flush speichert noch nicht endgültig,
    # gibt uns aber schon die neue Task-ID
    db.flush()

    # Je nach Kategorie werden die passenden Zusatzdaten gespeichert
    if task_data.category == TaskCategory.SHOPPING:
        if task_data.shopping_details is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Für eine Einkaufsanfrage werden Einkaufsdetails benötigt.",
            )

        details = ShoppingDetails(
            task_id=new_task.id,
            shopping_list=task_data.shopping_details.shopping_list,
            store=task_data.shopping_details.store,
        )

        db.add(details)

    elif task_data.category == TaskCategory.APPOINTMENT:
        if task_data.appointment_details is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Für eine Terminanfrage werden Termindetails benötigt.",
            )

        details = AppointmentDetails(
            task_id=new_task.id,
            location=task_data.appointment_details.location,
            appointment_type=task_data.appointment_details.appointment_type,
        )

        db.add(details)

    elif task_data.category == TaskCategory.FURNITURE:
        if task_data.furniture_details is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Für eine Möbelanfrage werden Möbeldetails benötigt.",
            )

        details = FurnitureDetails(
            task_id=new_task.id,
            weight_kg=task_data.furniture_details.weight_kg,
            floor=task_data.furniture_details.floor,
            elevator_available=task_data.furniture_details.elevator_available,
        )

        db.add(details)

    elif task_data.category == TaskCategory.CRAFT:
        if task_data.craft_details is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Für eine handwerkliche Anfrage werden zusätzliche Angaben benötigt.",
            )

        details = CraftDetails(
            task_id=new_task.id,
            work_type=task_data.craft_details.work_type,
            required_tools=task_data.craft_details.required_tools,
            difficulty=task_data.craft_details.difficulty,
        )

        db.add(details)

    # Erst jetzt wird Task + Detail gemeinsam dauerhaft gespeichert
    db.commit()
    db.refresh(new_task)

    return {
        "id": new_task.id,
        "title": new_task.title,
        "category": new_task.category,
        "status": new_task.status,
        "senior_id": new_task.senior_id,
    }