from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_senior, require_helper
from app.db.database import get_db
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskCategory

from sqlalchemy import select

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

# Diese Route ist nur für eingeloggte Helfer zugänglich
@router.post("/{task_id}/accept")
def accept_task(
    task_id: int,
    current_user: User = Depends(require_helper),
    db: Session = Depends(get_db),
):
    # Task anhand seiner ID suchen
    task = db.get(Task, task_id)

    # Prüfen, ob der Task überhaupt existiert
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task wurde nicht gefunden.",
        )

    # Nur offene Tasks dürfen angenommen werden
    if task.status != TaskStatus.OPEN.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dieser Task ist nicht mehr offen.",
        )

    # Eingeloggten Helfer eintragen
    task.helper_id = current_user.id

    # Status ändern
    task.status = TaskStatus.ACCEPTED.value

    db.commit()
    db.refresh(task)

    return task

@router.get("/open")
def get_open_tasks(
    current_user: User = Depends(require_helper),
    db: Session = Depends(get_db),
):
    open_tasks = db.scalars(
        select(Task).where(Task.status == TaskStatus.OPEN.value)
    ).all()

    return open_tasks